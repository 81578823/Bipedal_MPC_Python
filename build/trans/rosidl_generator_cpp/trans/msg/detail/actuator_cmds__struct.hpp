// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from trans:msg/ActuatorCmds.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__ACTUATOR_CMDS__STRUCT_HPP_
#define TRANS__MSG__DETAIL__ACTUATOR_CMDS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__trans__msg__ActuatorCmds __attribute__((deprecated))
#else
# define DEPRECATED__trans__msg__ActuatorCmds __declspec(deprecated)
#endif

namespace trans
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ActuatorCmds_
{
  using Type = ActuatorCmds_<ContainerAllocator>;

  explicit ActuatorCmds_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit ActuatorCmds_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _names_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _names_type names;
  using _gain_p_type =
    rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _gain_p_type gain_p;
  using _pos_des_type =
    rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _pos_des_type pos_des;
  using _gaid_d_type =
    rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _gaid_d_type gaid_d;
  using _vel_des_type =
    rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _vel_des_type vel_des;
  using _feedforward_torque_type =
    rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _feedforward_torque_type feedforward_torque;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__names(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->names = _arg;
    return *this;
  }
  Type & set__gain_p(
    const rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->gain_p = _arg;
    return *this;
  }
  Type & set__pos_des(
    const rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->pos_des = _arg;
    return *this;
  }
  Type & set__gaid_d(
    const rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->gaid_d = _arg;
    return *this;
  }
  Type & set__vel_des(
    const rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->vel_des = _arg;
    return *this;
  }
  Type & set__feedforward_torque(
    const rosidl_runtime_cpp::BoundedVector<double, 30, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->feedforward_torque = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    trans::msg::ActuatorCmds_<ContainerAllocator> *;
  using ConstRawPtr =
    const trans::msg::ActuatorCmds_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<trans::msg::ActuatorCmds_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<trans::msg::ActuatorCmds_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      trans::msg::ActuatorCmds_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<trans::msg::ActuatorCmds_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      trans::msg::ActuatorCmds_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<trans::msg::ActuatorCmds_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<trans::msg::ActuatorCmds_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<trans::msg::ActuatorCmds_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__trans__msg__ActuatorCmds
    std::shared_ptr<trans::msg::ActuatorCmds_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__trans__msg__ActuatorCmds
    std::shared_ptr<trans::msg::ActuatorCmds_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ActuatorCmds_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->names != other.names) {
      return false;
    }
    if (this->gain_p != other.gain_p) {
      return false;
    }
    if (this->pos_des != other.pos_des) {
      return false;
    }
    if (this->gaid_d != other.gaid_d) {
      return false;
    }
    if (this->vel_des != other.vel_des) {
      return false;
    }
    if (this->feedforward_torque != other.feedforward_torque) {
      return false;
    }
    return true;
  }
  bool operator!=(const ActuatorCmds_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ActuatorCmds_

// alias to use template instance with default allocator
using ActuatorCmds =
  trans::msg::ActuatorCmds_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace trans

#endif  // TRANS__MSG__DETAIL__ACTUATOR_CMDS__STRUCT_HPP_
