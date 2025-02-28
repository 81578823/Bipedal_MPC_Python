// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "trans/msg/detail/actuator_cmds__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace trans
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ActuatorCmds_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) trans::msg::ActuatorCmds(_init);
}

void ActuatorCmds_fini_function(void * message_memory)
{
  auto typed_message = static_cast<trans::msg::ActuatorCmds *>(message_memory);
  typed_message->~ActuatorCmds();
}

size_t size_function__ActuatorCmds__names(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<std::string> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ActuatorCmds__names(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<std::string> *>(untyped_member);
  return &member[index];
}

void * get_function__ActuatorCmds__names(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<std::string> *>(untyped_member);
  return &member[index];
}

void fetch_function__ActuatorCmds__names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const std::string *>(
    get_const_function__ActuatorCmds__names(untyped_member, index));
  auto & value = *reinterpret_cast<std::string *>(untyped_value);
  value = item;
}

void assign_function__ActuatorCmds__names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<std::string *>(
    get_function__ActuatorCmds__names(untyped_member, index));
  const auto & value = *reinterpret_cast<const std::string *>(untyped_value);
  item = value;
}

void resize_function__ActuatorCmds__names(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<std::string> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ActuatorCmds__gain_p(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ActuatorCmds__gain_p(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__ActuatorCmds__gain_p(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__ActuatorCmds__gain_p(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__ActuatorCmds__gain_p(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__ActuatorCmds__gain_p(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__ActuatorCmds__gain_p(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__ActuatorCmds__gain_p(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ActuatorCmds__pos_des(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ActuatorCmds__pos_des(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__ActuatorCmds__pos_des(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__ActuatorCmds__pos_des(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__ActuatorCmds__pos_des(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__ActuatorCmds__pos_des(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__ActuatorCmds__pos_des(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__ActuatorCmds__pos_des(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ActuatorCmds__gaid_d(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ActuatorCmds__gaid_d(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__ActuatorCmds__gaid_d(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__ActuatorCmds__gaid_d(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__ActuatorCmds__gaid_d(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__ActuatorCmds__gaid_d(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__ActuatorCmds__gaid_d(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__ActuatorCmds__gaid_d(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ActuatorCmds__vel_des(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ActuatorCmds__vel_des(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__ActuatorCmds__vel_des(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__ActuatorCmds__vel_des(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__ActuatorCmds__vel_des(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__ActuatorCmds__vel_des(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__ActuatorCmds__vel_des(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__ActuatorCmds__vel_des(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ActuatorCmds__feedforward_torque(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ActuatorCmds__feedforward_torque(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__ActuatorCmds__feedforward_torque(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__ActuatorCmds__feedforward_torque(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__ActuatorCmds__feedforward_torque(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__ActuatorCmds__feedforward_torque(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__ActuatorCmds__feedforward_torque(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__ActuatorCmds__feedforward_torque(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ActuatorCmds_message_member_array[7] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans::msg::ActuatorCmds, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "names",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(trans::msg::ActuatorCmds, names),  // bytes offset in struct
    nullptr,  // default value
    size_function__ActuatorCmds__names,  // size() function pointer
    get_const_function__ActuatorCmds__names,  // get_const(index) function pointer
    get_function__ActuatorCmds__names,  // get(index) function pointer
    fetch_function__ActuatorCmds__names,  // fetch(index, &value) function pointer
    assign_function__ActuatorCmds__names,  // assign(index, value) function pointer
    resize_function__ActuatorCmds__names  // resize(index) function pointer
  },
  {
    "gain_p",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans::msg::ActuatorCmds, gain_p),  // bytes offset in struct
    nullptr,  // default value
    size_function__ActuatorCmds__gain_p,  // size() function pointer
    get_const_function__ActuatorCmds__gain_p,  // get_const(index) function pointer
    get_function__ActuatorCmds__gain_p,  // get(index) function pointer
    fetch_function__ActuatorCmds__gain_p,  // fetch(index, &value) function pointer
    assign_function__ActuatorCmds__gain_p,  // assign(index, value) function pointer
    resize_function__ActuatorCmds__gain_p  // resize(index) function pointer
  },
  {
    "pos_des",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans::msg::ActuatorCmds, pos_des),  // bytes offset in struct
    nullptr,  // default value
    size_function__ActuatorCmds__pos_des,  // size() function pointer
    get_const_function__ActuatorCmds__pos_des,  // get_const(index) function pointer
    get_function__ActuatorCmds__pos_des,  // get(index) function pointer
    fetch_function__ActuatorCmds__pos_des,  // fetch(index, &value) function pointer
    assign_function__ActuatorCmds__pos_des,  // assign(index, value) function pointer
    resize_function__ActuatorCmds__pos_des  // resize(index) function pointer
  },
  {
    "gaid_d",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans::msg::ActuatorCmds, gaid_d),  // bytes offset in struct
    nullptr,  // default value
    size_function__ActuatorCmds__gaid_d,  // size() function pointer
    get_const_function__ActuatorCmds__gaid_d,  // get_const(index) function pointer
    get_function__ActuatorCmds__gaid_d,  // get(index) function pointer
    fetch_function__ActuatorCmds__gaid_d,  // fetch(index, &value) function pointer
    assign_function__ActuatorCmds__gaid_d,  // assign(index, value) function pointer
    resize_function__ActuatorCmds__gaid_d  // resize(index) function pointer
  },
  {
    "vel_des",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans::msg::ActuatorCmds, vel_des),  // bytes offset in struct
    nullptr,  // default value
    size_function__ActuatorCmds__vel_des,  // size() function pointer
    get_const_function__ActuatorCmds__vel_des,  // get_const(index) function pointer
    get_function__ActuatorCmds__vel_des,  // get(index) function pointer
    fetch_function__ActuatorCmds__vel_des,  // fetch(index, &value) function pointer
    assign_function__ActuatorCmds__vel_des,  // assign(index, value) function pointer
    resize_function__ActuatorCmds__vel_des  // resize(index) function pointer
  },
  {
    "feedforward_torque",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    30,  // array size
    true,  // is upper bound
    offsetof(trans::msg::ActuatorCmds, feedforward_torque),  // bytes offset in struct
    nullptr,  // default value
    size_function__ActuatorCmds__feedforward_torque,  // size() function pointer
    get_const_function__ActuatorCmds__feedforward_torque,  // get_const(index) function pointer
    get_function__ActuatorCmds__feedforward_torque,  // get(index) function pointer
    fetch_function__ActuatorCmds__feedforward_torque,  // fetch(index, &value) function pointer
    assign_function__ActuatorCmds__feedforward_torque,  // assign(index, value) function pointer
    resize_function__ActuatorCmds__feedforward_torque  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ActuatorCmds_message_members = {
  "trans::msg",  // message namespace
  "ActuatorCmds",  // message name
  7,  // number of fields
  sizeof(trans::msg::ActuatorCmds),
  ActuatorCmds_message_member_array,  // message members
  ActuatorCmds_init_function,  // function to initialize message memory (memory has to be allocated)
  ActuatorCmds_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ActuatorCmds_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ActuatorCmds_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace trans


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<trans::msg::ActuatorCmds>()
{
  return &::trans::msg::rosidl_typesupport_introspection_cpp::ActuatorCmds_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, trans, msg, ActuatorCmds)() {
  return &::trans::msg::rosidl_typesupport_introspection_cpp::ActuatorCmds_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
