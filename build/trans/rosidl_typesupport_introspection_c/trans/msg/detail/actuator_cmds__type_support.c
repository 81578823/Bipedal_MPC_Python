// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "trans/msg/detail/actuator_cmds__rosidl_typesupport_introspection_c.h"
#include "trans/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "trans/msg/detail/actuator_cmds__functions.h"
#include "trans/msg/detail/actuator_cmds__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `names`
#include "rosidl_runtime_c/string_functions.h"
// Member `gain_p`
// Member `pos_des`
// Member `gaid_d`
// Member `vel_des`
// Member `feedforward_torque`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  trans__msg__ActuatorCmds__init(message_memory);
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_fini_function(void * message_memory)
{
  trans__msg__ActuatorCmds__fini(message_memory);
}

size_t trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__names(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__names(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__names(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__names(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__names(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__names(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__gain_p(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__gain_p(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__gain_p(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__gain_p(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__gain_p(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__gain_p(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__gain_p(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__gain_p(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__pos_des(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__pos_des(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__pos_des(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__pos_des(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__pos_des(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__pos_des(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__pos_des(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__pos_des(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__gaid_d(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__gaid_d(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__gaid_d(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__gaid_d(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__gaid_d(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__gaid_d(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__gaid_d(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__gaid_d(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__vel_des(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__vel_des(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__vel_des(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__vel_des(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__vel_des(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__vel_des(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__vel_des(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__vel_des(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__feedforward_torque(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__feedforward_torque(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__feedforward_torque(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__feedforward_torque(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__feedforward_torque(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__feedforward_torque(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__feedforward_torque(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__feedforward_torque(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_member_array[7] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans__msg__ActuatorCmds, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "names",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans__msg__ActuatorCmds, names),  // bytes offset in struct
    NULL,  // default value
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__names,  // size() function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__names,  // get_const(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__names,  // get(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__names,  // fetch(index, &value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__names,  // assign(index, value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__names  // resize(index) function pointer
  },
  {
    "gain_p",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans__msg__ActuatorCmds, gain_p),  // bytes offset in struct
    NULL,  // default value
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__gain_p,  // size() function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__gain_p,  // get_const(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__gain_p,  // get(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__gain_p,  // fetch(index, &value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__gain_p,  // assign(index, value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__gain_p  // resize(index) function pointer
  },
  {
    "pos_des",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans__msg__ActuatorCmds, pos_des),  // bytes offset in struct
    NULL,  // default value
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__pos_des,  // size() function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__pos_des,  // get_const(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__pos_des,  // get(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__pos_des,  // fetch(index, &value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__pos_des,  // assign(index, value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__pos_des  // resize(index) function pointer
  },
  {
    "gaid_d",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans__msg__ActuatorCmds, gaid_d),  // bytes offset in struct
    NULL,  // default value
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__gaid_d,  // size() function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__gaid_d,  // get_const(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__gaid_d,  // get(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__gaid_d,  // fetch(index, &value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__gaid_d,  // assign(index, value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__gaid_d  // resize(index) function pointer
  },
  {
    "vel_des",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans__msg__ActuatorCmds, vel_des),  // bytes offset in struct
    NULL,  // default value
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__vel_des,  // size() function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__vel_des,  // get_const(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__vel_des,  // get(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__vel_des,  // fetch(index, &value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__vel_des,  // assign(index, value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__vel_des  // resize(index) function pointer
  },
  {
    "feedforward_torque",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans__msg__ActuatorCmds, feedforward_torque),  // bytes offset in struct
    NULL,  // default value
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__size_function__ActuatorCmds__feedforward_torque,  // size() function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_const_function__ActuatorCmds__feedforward_torque,  // get_const(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__get_function__ActuatorCmds__feedforward_torque,  // get(index) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__fetch_function__ActuatorCmds__feedforward_torque,  // fetch(index, &value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__assign_function__ActuatorCmds__feedforward_torque,  // assign(index, value) function pointer
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__resize_function__ActuatorCmds__feedforward_torque  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_members = {
  "trans__msg",  // message namespace
  "ActuatorCmds",  // message name
  7,  // number of fields
  sizeof(trans__msg__ActuatorCmds),
  trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_member_array,  // message members
  trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_init_function,  // function to initialize message memory (memory has to be allocated)
  trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_type_support_handle = {
  0,
  &trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_trans
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trans, msg, ActuatorCmds)() {
  trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_type_support_handle.typesupport_identifier) {
    trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &trans__msg__ActuatorCmds__rosidl_typesupport_introspection_c__ActuatorCmds_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
