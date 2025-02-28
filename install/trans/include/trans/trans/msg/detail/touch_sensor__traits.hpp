// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from trans:msg/TouchSensor.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__TOUCH_SENSOR__TRAITS_HPP_
#define TRANS__MSG__DETAIL__TOUCH_SENSOR__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "trans/msg/detail/touch_sensor__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace trans
{

namespace msg
{

inline void to_flow_style_yaml(
  const TouchSensor & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: names
  {
    if (msg.names.size() == 0) {
      out << "names: []";
    } else {
      out << "names: [";
      size_t pending_items = msg.names.size();
      for (auto item : msg.names) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: value
  {
    if (msg.value.size() == 0) {
      out << "value: []";
    } else {
      out << "value: [";
      size_t pending_items = msg.value.size();
      for (auto item : msg.value) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TouchSensor & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: names
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.names.size() == 0) {
      out << "names: []\n";
    } else {
      out << "names:\n";
      for (auto item : msg.names) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.value.size() == 0) {
      out << "value: []\n";
    } else {
      out << "value:\n";
      for (auto item : msg.value) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TouchSensor & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace trans

namespace rosidl_generator_traits
{

[[deprecated("use trans::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const trans::msg::TouchSensor & msg,
  std::ostream & out, size_t indentation = 0)
{
  trans::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use trans::msg::to_yaml() instead")]]
inline std::string to_yaml(const trans::msg::TouchSensor & msg)
{
  return trans::msg::to_yaml(msg);
}

template<>
inline const char * data_type<trans::msg::TouchSensor>()
{
  return "trans::msg::TouchSensor";
}

template<>
inline const char * name<trans::msg::TouchSensor>()
{
  return "trans/msg/TouchSensor";
}

template<>
struct has_fixed_size<trans::msg::TouchSensor>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<trans::msg::TouchSensor>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<trans::msg::TouchSensor>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // TRANS__MSG__DETAIL__TOUCH_SENSOR__TRAITS_HPP_
