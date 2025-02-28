// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__ACTUATOR_CMDS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define TRANS__MSG__DETAIL__ACTUATOR_CMDS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "trans/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "trans/msg/detail/actuator_cmds__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace trans
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_trans
cdr_serialize(
  const trans::msg::ActuatorCmds & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_trans
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  trans::msg::ActuatorCmds & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_trans
get_serialized_size(
  const trans::msg::ActuatorCmds & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_trans
max_serialized_size_ActuatorCmds(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace trans

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_trans
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, trans, msg, ActuatorCmds)();

#ifdef __cplusplus
}
#endif

#endif  // TRANS__MSG__DETAIL__ACTUATOR_CMDS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
