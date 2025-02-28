// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from trans:srv/GaitSwitch.idl
// generated code does not contain a copyright notice

#ifndef TRANS__SRV__DETAIL__GAIT_SWITCH__BUILDER_HPP_
#define TRANS__SRV__DETAIL__GAIT_SWITCH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "trans/srv/detail/gait_switch__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace trans
{

namespace srv
{

namespace builder
{

class Init_GaitSwitch_Request_gait_name
{
public:
  explicit Init_GaitSwitch_Request_gait_name(::trans::srv::GaitSwitch_Request & msg)
  : msg_(msg)
  {}
  ::trans::srv::GaitSwitch_Request gait_name(::trans::srv::GaitSwitch_Request::_gait_name_type arg)
  {
    msg_.gait_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::trans::srv::GaitSwitch_Request msg_;
};

class Init_GaitSwitch_Request_header
{
public:
  Init_GaitSwitch_Request_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GaitSwitch_Request_gait_name header(::trans::srv::GaitSwitch_Request::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_GaitSwitch_Request_gait_name(msg_);
  }

private:
  ::trans::srv::GaitSwitch_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::trans::srv::GaitSwitch_Request>()
{
  return trans::srv::builder::Init_GaitSwitch_Request_header();
}

}  // namespace trans


namespace trans
{

namespace srv
{

namespace builder
{

class Init_GaitSwitch_Response_is_success
{
public:
  Init_GaitSwitch_Response_is_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::trans::srv::GaitSwitch_Response is_success(::trans::srv::GaitSwitch_Response::_is_success_type arg)
  {
    msg_.is_success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::trans::srv::GaitSwitch_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::trans::srv::GaitSwitch_Response>()
{
  return trans::srv::builder::Init_GaitSwitch_Response_is_success();
}

}  // namespace trans

#endif  // TRANS__SRV__DETAIL__GAIT_SWITCH__BUILDER_HPP_
