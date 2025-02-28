// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from trans:msg/TouchSensor.idl
// generated code does not contain a copyright notice

#ifndef TRANS__MSG__DETAIL__TOUCH_SENSOR__STRUCT_HPP_
#define TRANS__MSG__DETAIL__TOUCH_SENSOR__STRUCT_HPP_

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
# define DEPRECATED__trans__msg__TouchSensor __attribute__((deprecated))
#else
# define DEPRECATED__trans__msg__TouchSensor __declspec(deprecated)
#endif

namespace trans
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TouchSensor_
{
  using Type = TouchSensor_<ContainerAllocator>;

  explicit TouchSensor_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit TouchSensor_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _names_type =
    rosidl_runtime_cpp::BoundedVector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, 10, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _names_type names;
  using _value_type =
    rosidl_runtime_cpp::BoundedVector<float, 10, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _value_type value;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__names(
    const rosidl_runtime_cpp::BoundedVector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, 10, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->names = _arg;
    return *this;
  }
  Type & set__value(
    const rosidl_runtime_cpp::BoundedVector<float, 10, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    trans::msg::TouchSensor_<ContainerAllocator> *;
  using ConstRawPtr =
    const trans::msg::TouchSensor_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<trans::msg::TouchSensor_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<trans::msg::TouchSensor_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      trans::msg::TouchSensor_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<trans::msg::TouchSensor_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      trans::msg::TouchSensor_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<trans::msg::TouchSensor_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<trans::msg::TouchSensor_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<trans::msg::TouchSensor_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__trans__msg__TouchSensor
    std::shared_ptr<trans::msg::TouchSensor_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__trans__msg__TouchSensor
    std::shared_ptr<trans::msg::TouchSensor_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TouchSensor_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->names != other.names) {
      return false;
    }
    if (this->value != other.value) {
      return false;
    }
    return true;
  }
  bool operator!=(const TouchSensor_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TouchSensor_

// alias to use template instance with default allocator
using TouchSensor =
  trans::msg::TouchSensor_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace trans

#endif  // TRANS__MSG__DETAIL__TOUCH_SENSOR__STRUCT_HPP_
