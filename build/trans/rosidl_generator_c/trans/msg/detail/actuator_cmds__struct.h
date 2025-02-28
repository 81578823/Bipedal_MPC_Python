// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__ACTUATOR_CMDS__STRUCT_H_
#define TRANS__MSG__DETAIL__ACTUATOR_CMDS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'names'
#include "rosidl_runtime_c/string.h"
// Member 'gain_p'
// Member 'pos_des'
// Member 'gaid_d'
// Member 'vel_des'
// Member 'feedforward_torque'
#include "rosidl_runtime_c/primitives_sequence.h"

// constants for array fields with an upper bound
// gain_p
enum
{
  trans__msg__ActuatorCmds__gain_p__MAX_SIZE = 30
};
// pos_des
enum
{
  trans__msg__ActuatorCmds__pos_des__MAX_SIZE = 30
};
// gaid_d
enum
{
  trans__msg__ActuatorCmds__gaid_d__MAX_SIZE = 30
};
// vel_des
enum
{
  trans__msg__ActuatorCmds__vel_des__MAX_SIZE = 30
};
// feedforward_torque
enum
{
  trans__msg__ActuatorCmds__feedforward_torque__MAX_SIZE = 30
};

/// Struct defined in msg/ActuatorCmds in the package trans.
typedef struct trans__msg__ActuatorCmds
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String__Sequence names;
  rosidl_runtime_c__double__Sequence gain_p;
  rosidl_runtime_c__double__Sequence pos_des;
  rosidl_runtime_c__double__Sequence gaid_d;
  rosidl_runtime_c__double__Sequence vel_des;
  rosidl_runtime_c__double__Sequence feedforward_torque;
} trans__msg__ActuatorCmds;

// Struct for a sequence of trans__msg__ActuatorCmds.
typedef struct trans__msg__ActuatorCmds__Sequence
{
  trans__msg__ActuatorCmds * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} trans__msg__ActuatorCmds__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TRANS__MSG__DETAIL__ACTUATOR_CMDS__STRUCT_H_
