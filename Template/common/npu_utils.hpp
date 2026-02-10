#ifndef __NPU_UTILS_HPP__
#define __NPU_UTILS_HPP__

#include <cstdlib>
#include <iostream>
#include <string>
#include <fstream>
#include <boost/program_options.hpp>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdfloat>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <drm/drm.h>
#include <stdfloat>
#include "xrt/xrt_bo.h"
#include "xrt/xrt_device.h"
#include "xrt/xrt_kernel.h"
#include "amdxdna_accel.h"
#include "buffer.hpp"
#include "debug_utils.hpp"
#include "experimental/xrt_kernel.h"
#include "experimental/xrt_ext.h"
#include "experimental/xrt_module.h"
#include "experimental/xrt_elf.h"
#include "xrt/xrt_graph.h"

#include "npu_instr_utils.hpp"

///@brief accel_user_desc
///@param xclbin_name name of the xclbin file
///@param instr_seq instruction sequence, an object of npu_sequence
///@see npu_sequence
typedef struct {
    std::string xclbin_name;
    npu_sequence instr_seq;
} accel_user_desc;

///@brief accel_kernel_desc
///@param xclbin xclbin object
///@param kernel kernel object
///@param context hardware context
///@see xrt::xclbin, xrt::kernel, xrt::hw_context
typedef struct {
    xrt::xclbin xclbin;
    xrt::kernel kernel;
    xrt::hw_context context;
} accel_kernel_desc;

///@brief accel_hw_desc
///@param instr_name name of the instruction sequence
///@param kernel_desc kernel descriptor
///@param bo_instr buffer object of the instruction sequence
///@param instr_size size of the instruction sequence
typedef struct {
    std::string instr_name;
    accel_kernel_desc* kernel_desc;
    xrt::bo bo_instr;
    size_t instr_size;
} accel_hw_desc;



///@brief npu_app
///@note There should be only one npu_app inside main.
///@note It handles all xclbins and instr_sequences.
///@note Each xclbin may have multiple instr_sequences.
///@note Each xclbin and instr_sequence has a unique id.
///@note Both id shall be provided to run an accelerator.
///@note Therefore, the xclbin_name between different accel_descriptions may overlap, but the instr_name is unique.
class npu_app{
public:
    constexpr static int max_xclbins = 16; // This is hard constraint from the XRT driver
    
    npu_app(int max_instrs = 1, unsigned int device_id = 0U);

    int register_accel_app(accel_user_desc& user_desc);
    ~npu_app();
    int _load_instr_sequence(accel_user_desc& user_desc, accel_hw_desc& hw_desc);
    int _load_xclbin(std::string xclbin_name);
    xrt::bo create_buffer(size_t size, int group_id, int app_id);

    void replace_instr(int app_id, npu_sequence& seq);

    template<typename T>
    buffer<T> create_bo_buffer(size_t size, int group_id, int app_id){
        LOG_VERBOSE(2, "Creating buffer buffer with size: " << size << " and group_id: " << group_id << " and app_id: " << app_id);
        return buffer<T>(size, this->device, this->hw_descs[app_id].kernel_desc->kernel, group_id);
    }

    template<typename... BoArgs>
    ert_cmd_state run(int app_id = 0, BoArgs&&... args){
        unsigned int opcode = 3;
        LOG_VERBOSE(3, "Running kernel with app_id: " << app_id);
        auto run = this->hw_descs[app_id].kernel_desc->kernel(opcode, this->hw_descs[app_id].bo_instr, this->hw_descs[app_id].instr_size, args...);
        ert_cmd_state r = run.wait();
        LOG_VERBOSE(3, "Kernel run finished with status: " << r);
        return r;
    }

    template<typename... BoArgs>
    xrt::run create_run(int app_id, BoArgs&&... args){
        xrt::run run = xrt::run(this->hw_descs[app_id].kernel_desc->kernel);
        run.set_arg(0, 3);
        run.set_arg(1, this->hw_descs[app_id].bo_instr);
        run.set_arg(2, this->hw_descs[app_id].instr_size);
        xrt::bo* bo_args[] = {&args...};
        for (int i = 0; i < sizeof...(args); i++){
            run.set_arg(3 + i, *bo_args[i]);
        }
        return run;
    }

    xrt::runlist create_runlist(int app_id);
    
    void list_kernels();
    void write_out_trace(char *traceOutPtr, size_t trace_size, std::string path);
    void print_npu_info();
    float get_npu_power(bool print = true);

    void interperate_bd(int app_id);

private:
    std::vector<accel_kernel_desc> kernel_descs;
    std::vector<accel_hw_desc> hw_descs;
    std::vector<std::string> registered_xclbin_names;

    int kernel_desc_count;
    int hw_desc_count;

    // the only device instance
    xrt::device device;
};

#endif
