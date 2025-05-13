


import json
import argparse
import os
from typing import NamedTuple, Tuple
import math

class MatrixConfig(NamedTuple):
    trace_size: int
    simulate_end_time: float
    switch_size: int
    diode_size: int
    u_size: int #input source 
    state_size: int 
    y_size: int # number of output
    iteration_steps: int
    total_switch_configs: int #2 **(switch+diode number)
    C1_DSW_col: int  #round up to multiple of 16
    C1_DSW_row: int
    C1_DSW_mat_size: int
    state_size_aligned: int
    y_size_aligned: int  # Y round up to 16
    ABCD_rows: int # rounded up to 16
    ABCD_cols: int # rounded up to 16
    ABCD_mat_size: int
    input_length_per_iter: int # number of float for each input
    output_length_per_iter: int # number of output for each input
    buffer_size_of_C1_DSW_matrixes: int # total number of float for switch_diode_matrix
    buffer_size_of_ABCD_matrixes: int # total number of float for abcd matrix

 
def MatrixConfig_to_dict(val:MatrixConfig):
    
    return   {
        "trace_size": val.trace_size,
        "state_size": val.state_size,
        "u_size": val.u_size,
        "y_size": val.y_size,
        "diode_size": val.diode_size,
        "switch_size": val.switch_size,
        "C1_DSW_row_size": val.C1_DSW_row,
        "C1_DSW_col_size": val.C1_DSW_col,
        "C1_DSW_matrix_size":val.C1_DSW_mat_size,
        "C1_DSW_buffer_size": val.buffer_size_of_C1_DSW_matrixes,
        
        "A_B_C_D_row_size": val.ABCD_rows,
        "A_B_C_D_col_size": val.ABCD_cols,
        "A_B_C_D_matrix_size": val.ABCD_mat_size,
        "A_B_C_D_buffer_size": val.buffer_size_of_ABCD_matrixes,
        
        "input_size_per_iteration": val.input_length_per_iter,
        "output_size_per_iteration": val.output_length_per_iter,
        "total_switch_diode_state": val.total_switch_configs,
        "iteration_step_number":val.iteration_steps,
        "state_size_ceil_to_16": val.state_size_aligned,
        "y_size_ceil_to_16":val.y_size_aligned,

        
    }         
   


def cpp_define(key, value):
    key = key.upper() 
    if isinstance(value, bool):
        return f"#define {key} {'1' if value else '0'}"
    elif isinstance(value, (int, float)):
        return f"#define {key} {value}"
    elif isinstance(value, str):
        return f'#define {key} "{value}"'
    else:
        raise TypeError(f"Unsupported type for key {key}: {type(value)}")

def generate_header(json_file, header_file):
    with open(json_file, "r") as f:
        config = json.load(f)

    with open(header_file, "w") as f:
        f.write("// Auto-generated config header\n")
        f.write("#ifndef CIRCUIT_CONFIG_H\n#define CIRCUIT_CONFIG_H\n\n")
        for key, value in config.items():
            f.write(cpp_define(key, value) + "\n")
        f.write("\n#endif // CIRCUIT_CONFIG_H\n")




def custom_floor(x, multiplier):
  return math.floor(x / multiplier) * multiplier

def custom_ceil(x, multiplier):
  return math.ceil(x / multiplier) * multiplier

def load_data_from_config(json_config_file:str):
    try:
        with open(json_config_file, "r") as f:
            config_data = json.load(f)
            print("Successfully loaded the JSON data from 'config.json':")
            print(config_data)

            # You can now access the individual parameters like this:
            trace_size = int(config_data.get("trace_size"))

            simulate_end_time = config_data.get("simulate_end_time")
            switch_size = config_data.get("switch_size")
            diode_size = config_data.get("diode_size")
            u_size = config_data.get("u_size")
            state_size = config_data.get("state_size")
            y_size = config_data.get("y_size")
            iteration_step_number = config_data.get("iteration_step_number")
            
        return trace_size, simulate_end_time, switch_size, diode_size, u_size, state_size, y_size, iteration_step_number
    except FileNotFoundError:
        print("Error: The file 'config.json' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in 'config.json': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
                    


def common_matrix_config(json_config_file:str):
    
    trace_size, simulate_end_time, switch_size, diode_size, u_size, state_size, y_size, iteration_step_number = load_data_from_config(json_config_file)

    total_switch_size = 2**(switch_size + diode_size)
    
    # For each diode, the matrix is      3*(diode_number) x (state_size+u_size)
    #NOTE: the host should already add (u_size) of column concat with C_diode_impulse_sw, if not memory reordering is not possible with constant stride in dma
    C1_DSW_col_size = (state_size+u_size) 
    C1_DSW_row_size =   custom_ceil(3* diode_size,16)
    C1_DSW_mat_size =  C1_DSW_col_size* C1_DSW_row_size
    # Iteration matrix consist of A_with_dep, B_with_dep, C_imp, C_natual, D_imp, D_natual

    # A_with_dep and B_with_dep can be combined into one matrix of size (state_size x (state_size+u_size))
    # And C_impulse_mat, D_impulse_mat can be combine into one matrix with of size (Y_size x(state_size + u_size))
    # and C_non_impulse_matrix, D_non_impulse_matrix can be combined into another matrix of size (Y_size x (state_size+u_size))
    
    state_size_ceil_to_16 = custom_ceil(state_size, 16)
    y_size_ceil_to_16 = custom_ceil(y_size, 16)
    A_B_C_D_mat_row =   state_size_ceil_to_16 +  y_size_ceil_to_16*2  # For ease of computation, use CEIL(,16) for all dimeison/size
    A_B_C_D_mat_col = (state_size + u_size)
    A_B_C_D_mat_size = A_B_C_D_mat_row * A_B_C_D_mat_col
    
    _len_of_switch_size = (custom_ceil(switch_size+diode_size,32)//32 )   # number of 4byte(float) use for sending external switch for each iteration
    len_of_input_for_each_iteration = u_size+ _len_of_switch_size
    len_of_output_for_each_iteration =y_size_ceil_to_16
    
    buffer_size_of_C1_DSW_matrix = total_switch_size*C1_DSW_mat_size
    buffer_A_B_C_D_size = total_switch_size * A_B_C_D_mat_size
    

    return MatrixConfig(
        trace_size=trace_size,
        simulate_end_time=simulate_end_time,
        switch_size=switch_size,
        diode_size=diode_size,
        u_size=u_size,
        state_size=state_size,
        y_size=y_size,
        iteration_steps=iteration_step_number,
        total_switch_configs=total_switch_size,
        C1_DSW_row=C1_DSW_row_size,
        C1_DSW_col=C1_DSW_col_size,
        C1_DSW_mat_size=C1_DSW_mat_size,
        state_size_aligned=state_size_ceil_to_16,
        y_size_aligned=y_size_ceil_to_16,
        ABCD_rows=A_B_C_D_mat_row,
        ABCD_cols=A_B_C_D_mat_col,
        ABCD_mat_size=A_B_C_D_mat_size,
        input_length_per_iter=len_of_input_for_each_iteration,
        output_length_per_iter=len_of_output_for_each_iteration,
        buffer_size_of_C1_DSW_matrixes=buffer_size_of_C1_DSW_matrix,
        buffer_size_of_ABCD_matrixes=buffer_A_B_C_D_size,
        
        
        
    )
    # return     trace_size, simulate_end_time, switch_size, diode_size, u_size, state_size, y_size, iteration_step_number,  total_switch_size,\
    #     C1_DSW_col_size, C1_DSW_row_size, C1_DSW_mat_size, state_size_ceil_to_16, y_size_ceil_to_16, A_B_C_D_mat_row, A_B_C_D_mat_col,\
    #         len_of_input_for_each_iteration, len_of_output_for_each_iteration, buffer_size_of_C1_DSW_matrix, buffer_A_B_C_D_size
            
            
def main_single_CT(json_config_file:str, output_json_file:str, output_header_file:str , override_memory_limit:bool):
    common_conf: MatrixConfig =common_matrix_config(json_config_file)
    
    #INTENDED to be allocated on stack for it
    buffer_size_of_cur_X_U = custom_ceil(  common_conf.state_size+ common_conf.u_size , 16)
    buffer_size_of_C1_DSW_mat_res = common_conf.C1_DSW_row  
    buffer_size_of_A_B_C_D_mat_res =common_conf.ABCD_rows  
    
    stack_size = 1024 # default value
    stack_size += (buffer_size_of_cur_X_U +buffer_size_of_C1_DSW_mat_res  + buffer_size_of_A_B_C_D_mat_res )*4 # 4 byte for float

    # note: because load 16 float at a time for vector instruction, need to ensure the address are aligned to 64byte(4*16)
    buffer_size_for_in_out_in_float = ((64)*(1024) - stack_size)//4 - (common_conf.buffer_size_of_C1_DSW_matrixes +common_conf.buffer_size_of_ABCD_matrixes)  # 4 byte for float
    # define a ping pong for it? 

    _max_iteration_step = int(custom_floor( buffer_size_for_in_out_in_float//(common_conf.input_length_per_iter + common_conf.output_length_per_iter),2)) #TODO: round down instead?
    if(_max_iteration_step < 2):
        if override_memory_limit:
            _max_iteration_step = 2
        else:
            raise ValueError("FATAIL, no enough memory left") 
    iteration_step_per_buffer = _max_iteration_step //2
    buffer_size_of_in_ping_pong = common_conf.input_length_per_iter*(iteration_step_per_buffer)
    buffer_size_of_out_ping_pong = common_conf.output_length_per_iter*(iteration_step_per_buffer)
    
    
    ping_pong_buffer_iteration =  math.ceil(common_conf.iteration_steps/iteration_step_per_buffer)
    print("Total number of ping pong buffer: ", ping_pong_buffer_iteration)
    
    # now write the final config result to file

    extracted_Data = {

        "iteration_step_per_ping_pong_buffer": iteration_step_per_buffer,
        "buffer_size_of_in_ping_poing": buffer_size_of_in_ping_pong,
        "buffer_size_of_out_ping_pong": buffer_size_of_out_ping_pong,
        "ping_pong_buffer_iteration": ping_pong_buffer_iteration,

        
        "buffer_size_of_cur_X_U": buffer_size_of_cur_X_U,
        "buffer_size_of_C1_DSW_mat_res":buffer_size_of_C1_DSW_mat_res,
        "buffer_size_of_A_B_C_D_mat_res": buffer_size_of_A_B_C_D_mat_res,
        "stack_size": stack_size
        
    }  | MatrixConfig_to_dict(common_conf)     
    with open(output_json_file,"w") as outfile:
        json.dump( extracted_Data, outfile, indent=4)
    
    
    generate_header(output_json_file, output_header_file)


        






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process circuit simulation configuration.")
    parser.add_argument("input_json", help="Path to the input configuration JSON file.")
    parser.add_argument("--final_json", default="final_config.json", help="Path to output processed JSON file.")
    parser.add_argument("--header", default="circuitConfig.h", help="Path to output C header file.")
    parser.add_argument("--override", default="FALSE", help="Option to consider the memory size limit on single CT")
    parser.add_argument("--CTNumber", default="1", help="number_of_CT_used")
    args = parser.parse_args()

    if args.override == "FALSE":
        override_opt = False
    else:
        override_opt = True
    if args.CTNumber == "1":
        main_single_CT(args.input_json, args.final_json, args.header,override_opt)
    else:
        raise ValueError("Unknown CT numbers")
        