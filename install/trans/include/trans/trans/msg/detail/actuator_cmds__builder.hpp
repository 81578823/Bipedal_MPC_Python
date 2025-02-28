// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__ACTUATOR_CMDS__BUILDER_HPP_
#define TRANS__MSG__DETAIL__ACTUATOR_CMDS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "trans/msg/detail/actuator_cmds__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace trans
{

namespace msg
{

namespace builder
{

class Init_ActuatorCmds_feedforward_torque
{
public:
  explicit Init_ActuatorCmds_feedforward_torque(::trans::msg::ActuatorCmds & msg)
  : msg_(msg)
  {}
  ::trans::msg::ActuatorCmds feedforward_torque(::trans::msg::ActuatorCmds::_feedforward_torque_type arg)
  {
    msg_.feedforward_torque = std::move(arg);
    return std::move(msg_);
  }

private:
  ::trans::msg::ActuatorCmds msg_;
};

class Init_ActuatorCmds_vel_des
{
public:
  explicit Init_ActuatorCmds_vel_des(::trans::msg::ActuatorCmds & msg)
  : msg_(msg)
  {}
  Init_ActuatorCmds_feedforward_torque vel_des(::trans::msg::ActuatorCmds::_vel_des_type arg)
  {
    msg_.vel_des = std::move(arg);
    return Init_ActuatorCmds_feedforward_torque(msg_);
  }

private:
  ::trans::msg::ActuatorCmds msg_;
};

class Init_ActuatorCmds_gaid_d
{
public:
  explicit Init_ActuatorCmds_gaid_d(::trans::msg::ActuatorCmds & msg)
  : msg_(msg)
  {}
  Init_ActuatorCmds_vel_des gaid_d(::trans::msg::ActuatorCmds::_gaid_d_type arg)
  {
    msg_.gaid_d = std::move(arg);
    return Init_ActuatorCmds_vel_des(msg_);
  }

private:
  ::trans::msg::ActuatorCmds msg_;
};

class Init_ActuatorCmds_pos_des
{
public:
  explicit Init_ActuatorCmds_pos_des(::trans::msg::ActuatorCmds & msg)
  : msg_(msg)
  {}
  Init_ActuatorCmds_gaid_d pos_des(::trans::msg::ActuatorCmds::_pos_des_type arg)
  {
    msg_.pos_des = std::move(arg);
    return Init_ActuatorCmds_gaid_d(msg_);
  }

private:
  ::trans::msg::ActuatorCmds msg_;
};

class Init_ActuatorCmds_gain_p
{
public:
  explicit Init_ActuatorCmds_gain_p(::trans::msg::ActuatorCmds & msg)
  : msg_(msg)
  {}
  Init_ActuatorCmds_pos_des gain_p(::trans::msg::ActuatorCmds::_gain_p_type arg)
  {
    msg_.gain_p = std::move(arg);
    return Init_ActuatorCmds_pos_des(msg_);
  }

private:
  ::trans::msg::ActuatorCmds msg_;
};

class Init_ActuatorCmds_names
{
public:
  explicit Init_ActuatorCmds_names(::trans::msg::ActuatorCmds & msg)
  : msg_(msg)
  {}
  Init_ActuatorCmds_gain_p names(::trans::msg::ActuatorCmds::_names_type arg)
  {
    msg_.names = std::move(arg);
    return Init_ActuatorCmds_gain_p(msg_);
  }

private:
  ::trans::msg::ActuatorCmds msg_;
};

class Init_ActuatorCmds_header
{
public:
  Init_ActuatorCmds_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ActuatorCmds_names header(::trans::msg::ActuatorCmds::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ActuatorCmds_names(msg_);
  }

private:
  ::trans::msg::ActuatorCmds msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::trans::msg::ActuatorCmds>()
{
  return trans::msg::builder::Init_ActuatorCmds_header();
}

}  // namespace trans

#endif  // TRANS__MSG__DETAIL__ACTUATOR_CMDS__BUILDER_HPP_
