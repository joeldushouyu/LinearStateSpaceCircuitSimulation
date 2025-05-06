#include <cstdint>
#include <iostream>
#include <bitset>


void extractLSBFirst3(const uint32_t* data, size_t N) {
    int total_bits = N * 32;
    int iterations = total_bits / 3;        // assume divisible by 3

    for (int i = 0; i < iterations; ++i) {
        int start_bit = 3 * i;              // 0, 3, 6, …
        uint32_t bits = extract_3bits_lsb_first(data, N, start_bit);
        std::cout 
            << "Iteration " << i 
            << ": bits [" << (start_bit+2) << "-" << start_bit << "] = "
            << std::bitset<3>(bits) 
            << "\n";
    }
}

int main() {
    // 96‑bit example:
    uint32_t arr96[3] = {
        0xF0F0F0F0,  // word 0 = bits 31–0  (LSW)
        0xAAAAAAAA,  // word 1 = bits 63–32
        0x12345678   // word 2 = bits 95–64 (MSW)
    };
    extractLSBFirst3(arr96, 3);
    return 0;
}