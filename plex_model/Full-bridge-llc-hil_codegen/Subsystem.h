/*
 * Header file for: Full-bridge-llc-hil/Subsystem
 * Generated with : PLECS 4.9.2
 * Generated on   : 8 Apr 2025 13:11:15
 */
#ifndef PLECS_HEADER_Subsystem_h_
#define PLECS_HEADER_Subsystem_h_

#include <stdbool.h>
#include <stdint.h>

/* Model floating point type */
typedef float Subsystem_FloatType;

/* Model checksum */
extern const char * const Subsystem_checksum;

/* Model error status */
extern const char * Subsystem_errorStatus;


/* Model sample time */
extern const float Subsystem_sampleTime;


/*
 * Model states */
typedef struct
{
   float Subsystem_PM0_x[6];        /* Subsystem */
   bool Subsystem_i1_PM0_s[8];      /* Subsystem */
} Subsystem_ModelStates;
extern Subsystem_ModelStates Subsystem_X;


/* External inputs */
typedef struct
{
   float Pulse;                     /* Subsystem/Pulse */
   float Pulse1;                    /* Subsystem/Pulse1 */
} Subsystem_ExternalInputs;
extern Subsystem_ExternalInputs Subsystem_U;


/* External outputs */
typedef struct
{
   float AMLr;                      /* Subsystem/AM Lr */
   float VMC;                       /* Subsystem/VM c */
   float VMD1;                      /* Subsystem/VM D1 */
   float VMD2;                      /* Subsystem/VM D2 */
   float VMD3;                      /* Subsystem/VM D3 */
   float VMD4;                      /* Subsystem/VM D4 */
   float VMOut;                     /* Subsystem/VM out */
   float AMD1;                      /* Subsystem/AM D1 */
   float AMD2;                      /* Subsystem/AM D2 */
   float AMD3;                      /* Subsystem/AM D3 */
   float AMD4;                      /* Subsystem/AM D4 */
   float AMIo;                      /* Subsystem/AM io */
} Subsystem_ExternalOutputs;
extern Subsystem_ExternalOutputs Subsystem_Y;


/* Block outputs */
typedef struct
{
   bool DataType;                   /* Subsystem/Data Type */
   bool DataType1;                  /* Subsystem/Data Type1 */
} Subsystem_BlockOutputs;
extern Subsystem_BlockOutputs Subsystem_B;

/* Entry point functions */
void Subsystem_initialize(float time);
void Subsystem_step(void);
void Subsystem_terminate(void);

#endif /* PLECS_HEADER_Subsystem_h_ */
