// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from trans:msg/TouchSensor.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__TOUCH_SENSOR__BUILDER_HPP_
#define TRANS__MSG__DETAIL__TOUCH_SENSOR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "trans/msg/detail/touch_sensor__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace trans
{

namespace msg
{

namespace builder
{

class Init_TouchSensor_value
{
public:
  explicit Init_TouchSensor_value(::trans::msg::TouchSensor & msg)
  : msg_(msg)
  {}
  ::trans::msg::TouchSensor value(::trans::msg::TouchSensor::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::trans::msg::TouchSensor msg_;
};

class Init_TouchSensor_names
{
public:
  explicit Init_TouchSensor_names(::trans::msg::TouchSensor & msg)
  : msg_(msg)
  {}
  Init_TouchSensor_value names(::trans::msg::TouchSensor::_names_type arg)
  {
    msg_.names = std::move(arg);
    return Init_TouchSensor_value(msg_);
  }

private:
  ::trans::msg::TouchSensor msg_;
};

class Init_TouchSensor_header
{
public:
  Init_TouchSensor_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TouchSensor_names header(::trans::msg::TouchSensor::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TouchSensor_names(msg_);
  }

private:
  ::trans::msg::TouchSensor msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::trans::msg::TouchSensor>()
{
  return trans::msg::builder::Init_TouchSensor_header();
}

}  // namespace trans

#endif  // TRANS__MSG__DETAIL__TOUCH_SENSOR__BUILDER_HPP_
