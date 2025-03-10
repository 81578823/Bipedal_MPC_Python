// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from trans:srv/SimulationReset.idl
// generated code does not contain a copyright notice

#ifndef TRANS__SRV__DETAIL__SIMULATION_RESET__TRAITS_HPP_
#define TRANS__SRV__DETAIL__SIMULATION_RESET__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "trans/srv/detail/simulation_reset__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'base_pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"
// Member 'joint_state'
#include "sensor_msgs/msg/detail/joint_state__traits.hpp"

namespace trans
{

namespace srv
{

inline void to_flow_style_yaml(
  const SimulationReset_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: base_pose
  {
    out << "base_pose: ";
    to_flow_style_yaml(msg.base_pose, out);
    out << ", ";
  }

  // member: joint_state
  {
    out << "joint_state: ";
    to_flow_style_yaml(msg.joint_state, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SimulationReset_Request & msg,
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

  // member: base_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "base_pose:\n";
    to_block_style_yaml(msg.base_pose, out, indentation + 2);
  }

  // member: joint_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "joint_state:\n";
    to_block_style_yaml(msg.joint_state, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SimulationReset_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace trans

namespace rosidl_generator_traits
{

[[deprecated("use trans::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const trans::srv::SimulationReset_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  trans::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use trans::srv::to_yaml() instead")]]
inline std::string to_yaml(const trans::srv::SimulationReset_Request & msg)
{
  return trans::srv::to_yaml(msg);
}

template<>
inline const char * data_type<trans::srv::SimulationReset_Request>()
{
  return "trans::srv::SimulationReset_Request";
}

template<>
inline const char * name<trans::srv::SimulationReset_Request>()
{
  return "trans/srv/SimulationReset_Request";
}

template<>
struct has_fixed_size<trans::srv::SimulationReset_Request>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Pose>::value && has_fixed_size<sensor_msgs::msg::JointState>::value && has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<trans::srv::SimulationReset_Request>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Pose>::value && has_bounded_size<sensor_msgs::msg::JointState>::value && has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<trans::srv::SimulationReset_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace trans
{

namespace srv
{

inline void to_flow_style_yaml(
  const SimulationReset_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: is_success
  {
    out << "is_success: ";
    rosidl_generator_traits::value_to_yaml(msg.is_success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SimulationReset_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: is_success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_success: ";
    rosidl_generator_traits::value_to_yaml(msg.is_success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SimulationReset_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace trans

namespace rosidl_generator_traits
{

[[deprecated("use trans::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const trans::srv::SimulationReset_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  trans::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use trans::srv::to_yaml() instead")]]
inline std::string to_yaml(const trans::srv::SimulationReset_Response & msg)
{
  return trans::srv::to_yaml(msg);
}

template<>
inline const char * data_type<trans::srv::SimulationReset_Response>()
{
  return "trans::srv::SimulationReset_Response";
}

template<>
inline const char * name<trans::srv::SimulationReset_Response>()
{
  return "trans/srv/SimulationReset_Response";
}

template<>
struct has_fixed_size<trans::srv::SimulationReset_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<trans::srv::SimulationReset_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<trans::srv::SimulationReset_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<trans::srv::SimulationReset>()
{
  return "trans::srv::SimulationReset";
}

template<>
inline const char * name<trans::srv::SimulationReset>()
{
  return "trans/srv/SimulationReset";
}

template<>
struct has_fixed_size<trans::srv::SimulationReset>
  : std::integral_constant<
    bool,
    has_fixed_size<trans::srv::SimulationReset_Request>::value &&
    has_fixed_size<trans::srv::SimulationReset_Response>::value
  >
{
};

template<>
struct has_bounded_size<trans::srv::SimulationReset>
  : std::integral_constant<
    bool,
    has_bounded_size<trans::srv::SimulationReset_Request>::value &&
    has_bounded_size<trans::srv::SimulationReset_Response>::value
  >
{
};

template<>
struct is_service<trans::srv::SimulationReset>
  : std::true_type
{
};

template<>
struct is_service_request<trans::srv::SimulationReset_Request>
  : std::true_type
{
};

template<>
struct is_service_response<trans::srv::SimulationReset_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // TRANS__SRV__DETAIL__SIMULATION_RESET__TRAITS_HPP_
