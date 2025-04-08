/*
 * Header file for: Full-bridge-llc-simplified-hil/Subsystem
 * Generated with : PLECS 4.9.2
 * Generated on   : 8 Apr 2025 13:07:06
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
   float Subsystem_PM0_x[7];        /* Subsystem */
   bool Subsystem_i1_PM0_s[4];      /* Subsystem */
} Subsystem_ModelStates;
extern Subsystem_ModelStates Subsystem_X;


/* External inputs */
typedef struct
{
   float SW1;                       /* Subsystem/SW 1 */
   float SW2;                       /* Subsystem/SW 2 */
} Subsystem_ExternalInputs;
extern Subsystem_ExternalInputs Subsystem_U;


/* External outputs */
typedef struct
{
   float VMOut;                     /* Subsystem/VM out */
   float VMD1;                      /* Subsystem/VM D1 */
   float VMD2;                      /* Subsystem/VM D2 */
   float AMLr;                      /* Subsystem/AM lr */
   float AMD1;                      /* Subsystem/AM D1 */
   float AMD2;                      /* Subsystem/AM D2 */
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
void Subsystem_output(void);
void Subsystem_update(void);
void Subsystem_terminate(void);

#endif /* PLECS_HEADER_Subsystem_h_ */
