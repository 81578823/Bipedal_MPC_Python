// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__ACTUATOR_CMDS__TRAITS_HPP_
#define TRANS__MSG__DETAIL__ACTUATOR_CMDS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "trans/msg/detail/actuator_cmds__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace trans
{

namespace msg
{

inline void to_flow_style_yaml(
  const ActuatorCmds & msg,
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

  // member: gain_p
  {
    if (msg.gain_p.size() == 0) {
      out << "gain_p: []";
    } else {
      out << "gain_p: [";
      size_t pending_items = msg.gain_p.size();
      for (auto item : msg.gain_p) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: pos_des
  {
    if (msg.pos_des.size() == 0) {
      out << "pos_des: []";
    } else {
      out << "pos_des: [";
      size_t pending_items = msg.pos_des.size();
      for (auto item : msg.pos_des) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: gaid_d
  {
    if (msg.gaid_d.size() == 0) {
      out << "gaid_d: []";
    } else {
      out << "gaid_d: [";
      size_t pending_items = msg.gaid_d.size();
      for (auto item : msg.gaid_d) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: vel_des
  {
    if (msg.vel_des.size() == 0) {
      out << "vel_des: []";
    } else {
      out << "vel_des: [";
      size_t pending_items = msg.vel_des.size();
      for (auto item : msg.vel_des) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: feedforward_torque
  {
    if (msg.feedforward_torque.size() == 0) {
      out << "feedforward_torque: []";
    } else {
      out << "feedforward_torque: [";
      size_t pending_items = msg.feedforward_torque.size();
      for (auto item : msg.feedforward_torque) {
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
  const ActuatorCmds & msg,
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

  // member: gain_p
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.gain_p.size() == 0) {
      out << "gain_p: []\n";
    } else {
      out << "gain_p:\n";
      for (auto item : msg.gain_p) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: pos_des
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.pos_des.size() == 0) {
      out << "pos_des: []\n";
    } else {
      out << "pos_des:\n";
      for (auto item : msg.pos_des) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: gaid_d
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.gaid_d.size() == 0) {
      out << "gaid_d: []\n";
    } else {
      out << "gaid_d:\n";
      for (auto item : msg.gaid_d) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: vel_des
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.vel_des.size() == 0) {
      out << "vel_des: []\n";
    } else {
      out << "vel_des:\n";
      for (auto item : msg.vel_des) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: feedforward_torque
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.feedforward_torque.size() == 0) {
      out << "feedforward_torque: []\n";
    } else {
      out << "feedforward_torque:\n";
      for (auto item : msg.feedforward_torque) {
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

inline std::string to_yaml(const ActuatorCmds & msg, bool use_flow_style = false)
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
  const trans::msg::ActuatorCmds & msg,
  std::ostream & out, size_t indentation = 0)
{
  trans::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use trans::msg::to_yaml() instead")]]
inline std::string to_yaml(const trans::msg::ActuatorCmds & msg)
{
  return trans::msg::to_yaml(msg);
}

template<>
inline const char * data_type<trans::msg::ActuatorCmds>()
{
  return "trans::msg::ActuatorCmds";
}

template<>
inline const char * name<trans::msg::ActuatorCmds>()
{
  return "trans/msg/ActuatorCmds";
}

template<>
struct has_fixed_size<trans::msg::ActuatorCmds>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<trans::msg::ActuatorCmds>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<trans::msg::ActuatorCmds>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // TRANS__MSG__DETAIL__ACTUATOR_CMDS__TRAITS_HPP_
