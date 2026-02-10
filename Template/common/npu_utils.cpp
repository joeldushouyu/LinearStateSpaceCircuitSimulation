#include "npu_utils.hpp"

///@brief constructor
///@param max_instrs maximum number of instr_sequences
///@param device_id device id default to 0, almost always 0
npu_app::npu_app(int max_instrs, unsigned int device_id){
    this->device = xrt::device(device_id);
    this->kernel_descs.resize(max_instrs);
    this->hw_descs.resize(max_instrs);
    this->registered_xclbin_names.clear();
    this->kernel_desc_count = 0;
    this->hw_desc_count = 0;
}

///@brief register an accel_user_desc to the npu_app
///@param user_desc accel_user_desc to be registered
///@return the app id of the registered accel_user_desc
///@note Different apps may have the same xclbin, but the sequence is unique.
///@note To avoid creating duplicated applications, the function checks if the xclbin is registered.
///@note If the xclbin is not registered, the function will register the xclbin and create a new application.
///@note If the xclbin is registered, the function will create a new application and load the instruction sequence.
int npu_app::register_accel_app(accel_user_desc& user_desc){
    assert(user_desc.instr_seq.name() != "");
    int xclbin_id = -1;
    for (int i = 0; i < this->registered_xclbin_names.size(); i++){
        if (this->registered_xclbin_names[i] == user_desc.xclbin_name){
            xclbin_id = i;
            break;
        }
    }
    LOG_VERBOSE_IF_ELSE(2, xclbin_id > -1, 
        "Found xclbin: " << user_desc.xclbin_name << "registered as id " << xclbin_id << "!",
        "Xclbin: " << user_desc.xclbin_name << " not registered yet!"
    );

    if (xclbin_id == -1){ // the xclbin is not registered yet
        if (this->kernel_desc_count >= this->kernel_descs.size()){
            throw std::runtime_error("Max number of xclbins reached");
        }
        if (_load_xclbin(user_desc.xclbin_name) != 0){
            std::cout<< "Load " << user_desc.xclbin_name << "ERROR!" << std::endl;
            exit(-1);
        }
        this->registered_xclbin_names.push_back(user_desc.xclbin_name);
        xclbin_id = this->registered_xclbin_names.size() - 1;
        LOG_VERBOSE(2, "Xclbin: " << user_desc.xclbin_name << " registered as id " << xclbin_id << "!");
        this->kernel_desc_count++;
    }
    // register the instr
    int app_id = -1;
    for (int i = 0; i < this->hw_descs.size(); i++){
        if (this->hw_descs[i].instr_name == user_desc.instr_seq.name()){
            app_id = i;
            break;
        }
    }
    LOG_VERBOSE_IF_ELSE(2, app_id > -1, 
        "Found instruction: " << user_desc.instr_seq.name() << "registered as id " << app_id << "!",
        "Instruction: " << user_desc.instr_seq.name() << " not registered yet!"
    );
    if (app_id == -1){ // instr is not registered yet
        if (this->hw_desc_count >= this->hw_descs.size()){
            throw std::runtime_error("Max number of instructions reached");
        }
        this->hw_descs[this->hw_desc_count].kernel_desc = &(this->kernel_descs[xclbin_id]);
        _load_instr_sequence(user_desc, this->hw_descs[this->hw_desc_count]);
        app_id = this->hw_desc_count;
        LOG_VERBOSE(2, "Instruction: " << user_desc.instr_name << " registered as id " << app_id << "!");
        this->hw_desc_count++;
    }
    return app_id;
}

///@brief load the instruction sequence to the buffer object
///@param user_desc accel_user_desc to be loaded
///@param hw_desc accel_hw_desc to be loaded
///@return 0 if successful
int npu_app::_load_instr_sequence(accel_user_desc& user_desc, accel_hw_desc& hw_desc){
    buffer<uint32_t> instr_v = user_desc.instr_seq.to_bo();
    hw_desc.bo_instr = xrt::bo(this->device, instr_v.size() * sizeof(int), XCL_BO_FLAGS_CACHEABLE, hw_desc.kernel_desc->kernel.group_id(1));
    void *bufInstr = hw_desc.bo_instr.map<void *>();
    memcpy(bufInstr, instr_v.data(), instr_v.size() * sizeof(int));
    hw_desc.bo_instr.sync(XCL_BO_SYNC_BO_TO_DEVICE);
    hw_desc.instr_size = instr_v.size();
    hw_desc.instr_name = user_desc.instr_seq.name();
    LOG_VERBOSE(2, "Instruction sequence loaded successfully!");
    return 0;
}

///@brief load the xclbin to the kernel descriptor
///@param xclbin_name name of the xclbin file
///@return 0 if successful
int npu_app::_load_xclbin(std::string xclbin_name){
    LOG_VERBOSE(2, "Loading xclbin: " << xclbin_name);
    this->kernel_descs[this->kernel_desc_count].xclbin = xrt::xclbin(xclbin_name);
    // int verbosity = VERBOSE;
    std::string Node = "MLIR_AIE";
    auto xkernels = this->kernel_descs[this->kernel_desc_count].xclbin.get_kernels();
    auto xkernel = *std::find_if(
        xkernels.begin(), 
        xkernels.end(),
        [Node](xrt::xclbin::kernel &k) {
            auto name = k.get_name();
            return name.rfind(Node, 0) == 0;
        }
    );
    this->device.register_xclbin(this->kernel_descs[this->kernel_desc_count].xclbin);
    auto kernelName = xkernel.get_name();
    this->kernel_descs[this->kernel_desc_count].context = xrt::hw_context(this->device, this->kernel_descs[this->kernel_desc_count].xclbin.get_uuid());
    this->kernel_descs[this->kernel_desc_count].kernel = xrt::kernel(this->kernel_descs[this->kernel_desc_count].context, kernelName);
    LOG_VERBOSE(2, "Xclbin: " << xclbin_name << " loaded successfully!");
    return 0;
}

///@brief create a xrt::bo buffer object
///@param size size of the buffer, unit is bytes
///@param group_id group id of the buffer
///@param app_id which application the buffer belongs to
///@return the buffer object
xrt::bo npu_app::create_buffer(size_t size, int group_id, int app_id){
    LOG_VERBOSE(2, "Creating buffer with size: " << size << " and group_id: " << group_id << " and app_id: " << app_id);
    if (app_id >= this->hw_descs.size()){
        throw std::runtime_error("App ID is out of range");
    }
    return xrt::bo(this->device, size, XRT_BO_FLAGS_HOST_ONLY, this->hw_descs[app_id].kernel_desc->kernel.group_id(group_id));
}

///@brief replace the instruction sequence with the new one
///@param app_id which application the instruction sequence belongs to
///@param seq new instruction sequence
///@note The function will replace the instruction sequence with the new one and update the buffer object.
void npu_app::replace_instr(int app_id, npu_sequence& seq){
    // replace the instruction sequence with the new one
    std::vector<uint32_t> instr_v = seq.to_npu();
    this->hw_descs[app_id].bo_instr = xrt::bo(this->device, instr_v.size() * sizeof(int), XCL_BO_FLAGS_CACHEABLE, this->hw_descs[app_id].kernel_desc->kernel.group_id(1));
    void *bufInstr = this->hw_descs[app_id].bo_instr.map<void *>();
    memcpy(bufInstr, instr_v.data(), instr_v.size() * sizeof(int));
    this->hw_descs[app_id].bo_instr.sync(XCL_BO_SYNC_BO_TO_DEVICE);
    this->hw_descs[app_id].instr_size = instr_v.size();
    this->hw_descs[app_id].instr_name = seq.name();
}

///@brief create a xrt::runlist object
///@param app_id which application the runlist belongs to
///@return the runlist object
///@note The function will create a xrt::runlist object with the context of the application.
xrt::runlist npu_app::create_runlist(int app_id){
    return xrt::runlist(this->hw_descs[app_id].kernel_desc->context);
}

///@brief destructor
///@note The function will destroy the kernel, buffer object and context.
npu_app::~npu_app(){
    // std::cout<<"clear bin!" << std::endl;
    // this->kernel.~kernel();
    // this->bo_instr.~bo();
    // this->context.~hw_context();
}

///@brief list the kernels and instruction sequences
void npu_app::list_kernels(){
    std::cout << "Listing kernels: (Total: " << this->hw_descs.size() << ")" << std::endl;
    for (int i = 0; i < this->hw_descs.size(); i++){
        std::cout << "Instruction " << i << ": " << this->hw_descs[i].instr_name << std::endl;
    }
    std::cout << "Listing xclbins: (Total: " << this->kernel_descs.size() << ")" << std::endl;
    for (int i = 0; i < this->kernel_descs.size(); i++){
        std::cout << "Xclbin " << i << " at address: " <<  &this->kernel_descs[i].xclbin << std::endl;
    }
}

///@brief write out the trace to a file
void npu_app::write_out_trace(char *traceOutPtr, size_t trace_size, std::string path) {
  std::ofstream fout(path);
  LOG_VERBOSE(1, "Writing out trace to: " << path);
  uint32_t *traceOut = (uint32_t *)traceOutPtr;
  for (int i = 0; i < trace_size / sizeof(traceOut[0]); i++) {
    fout << std::setfill('0') << std::setw(8) << std::hex << (int)traceOut[i];
    fout << std::endl;
  }
  fout.close();
  LOG_VERBOSE(1, "Trace written successfully!");
}

///@brief print the npu information
///@note The function will print the npu version, clock frequency, column count, row count, core info, mem info, shim info.
///@note The information is read via the IOCTL interface.
void npu_app::print_npu_info(){
    int fd = open("/dev/accel/accel0", O_RDWR);
    if (fd < 0) {
        perror("Failed to open amdgpu device");
        return;
    }
    amdxdna_drm_query_clock_metadata query_clock_metadata;
    amdxdna_drm_get_info get_info = {
        .param = DRM_AMDXDNA_QUERY_CLOCK_METADATA,
        .buffer_size = sizeof(amdxdna_drm_query_clock_metadata),
        .buffer = (unsigned long)&query_clock_metadata,
    };
    int ret = ioctl(fd, DRM_IOCTL_AMDXDNA_GET_INFO, &get_info);
    if (ret < 0) {
        std::cout << "Error code: " << ret << std::endl;
        perror("Failed to get telemetry information");
        close(fd);
        return;
    }

    amdxdna_drm_query_aie_metadata query_aie_metadata;
    get_info.param = DRM_AMDXDNA_QUERY_AIE_METADATA;
    get_info.buffer_size = sizeof(amdxdna_drm_query_aie_metadata);
    get_info.buffer = (unsigned long)&query_aie_metadata;
    ret = ioctl(fd, DRM_IOCTL_AMDXDNA_GET_INFO, &get_info);
    if (ret < 0) {
        std::cout << "Error code: " << ret << std::endl;
        perror("Failed to get telemetry information");
        close(fd);
        return;
    }

    close(fd);
    MSG_BONDLINE(40);
    MSG_BOX_LINE(40, "NPU version: " << query_aie_metadata.version.major << "." << query_aie_metadata.version.minor);
    MSG_BOX_LINE(40, "MP-NPU clock frequency: " << query_clock_metadata.mp_npu_clock.freq_mhz << " MHz");
    MSG_BOX_LINE(40, "H clock frequency: " << query_clock_metadata.h_clock.freq_mhz << " MHz");
    // What is the meaning of the column size?
    // std::cout << "NPU column size: " << query_aie_metadata.col_size << std::endl;
    MSG_BOX_LINE(40, "NPU column count: " << query_aie_metadata.cols);
    MSG_BOX_LINE(40, "NPU row count: " << query_aie_metadata.rows);
    MSG_BOX_LINE(40, "NPU core Info: ");
    MSG_BOX_LINE(40, "--Row count: " << query_aie_metadata.core.row_count);
    MSG_BOX_LINE(40, "--Row start: " << query_aie_metadata.core.row_start);
    MSG_BOX_LINE(40, "--DMA channel count: " << query_aie_metadata.core.dma_channel_count);
    MSG_BOX_LINE(40, "--Lock count: " << query_aie_metadata.core.lock_count);
    MSG_BOX_LINE(40, "--Event reg count: " << query_aie_metadata.core.event_reg_count);
    MSG_BOX_LINE(40, "NPU mem Info: ");
    MSG_BOX_LINE(40, "--Row count: " << query_aie_metadata.mem.row_count);
    MSG_BOX_LINE(40, "--Row start: " << query_aie_metadata.mem.row_start);
    MSG_BOX_LINE(40, "--DMA channel count: " << query_aie_metadata.mem.dma_channel_count);
    MSG_BOX_LINE(40, "--Lock count: " << query_aie_metadata.mem.lock_count);
    MSG_BOX_LINE(40, "--Event reg count: " << query_aie_metadata.mem.event_reg_count);
    MSG_BOX_LINE(40, "NPU shim Info: ");
    MSG_BOX_LINE(40, "--Row count: " << query_aie_metadata.shim.row_count);
    MSG_BOX_LINE(40, "--Row start: " << query_aie_metadata.shim.row_start);
    MSG_BOX_LINE(40, "--DMA channel count: " << query_aie_metadata.shim.dma_channel_count);
    MSG_BOX_LINE(40, "--Lock count: " << query_aie_metadata.shim.lock_count);
    MSG_BOX_LINE(40, "--Event reg count: " << query_aie_metadata.shim.event_reg_count);
    MSG_BONDLINE(40);
}

///@brief get the npu power consumption
///@param print whether to print the power consumption
///@return the power consumption, unit is Watt
float npu_app::get_npu_power(bool print){
    // get the npu power consumption, unit is Watt
    int fd = open("/dev/accel/accel0", O_RDWR);
    if (fd < 0) {
        perror("Failed to open amdgpu device");
        return -1;
    }
    amdxdna_drm_query_sensor query_sensor;

    amdxdna_drm_get_info get_info = {
        .param = DRM_AMDXDNA_QUERY_SENSORS,
        .buffer_size = sizeof(amdxdna_drm_query_sensor),
        .buffer = (unsigned long)&query_sensor,
    };
    int ret = ioctl(fd, DRM_IOCTL_AMDXDNA_GET_INFO, &get_info);
    if (ret < 0) {
        std::cout << "Error code: " << ret << std::endl;
        perror("Failed to get telemetry information");
        close(fd);
        return -1;
    }
    if (print){
        MSG_BOX(40, "NPU power: " << query_sensor.input << " " << query_sensor.units);
    }
    close(fd);
    return (float)query_sensor.input * pow(10, query_sensor.unitm);
}

///@brief interperate the buffer object to a npu_sequence
///@param app_id which application the buffer object belongs to
///@note The function will sync the buffer object from the device to the host and print the sequence.
void npu_app::interperate_bd(int app_id){
    // sync from the device to be consistent
    this->hw_descs[app_id].bo_instr.sync(XCL_BO_SYNC_BO_FROM_DEVICE);
    npu_sequence seq(this->hw_descs[app_id].bo_instr);
    seq.print_sequence();

    // verify the sequence.
    seq.to_npu();
}
