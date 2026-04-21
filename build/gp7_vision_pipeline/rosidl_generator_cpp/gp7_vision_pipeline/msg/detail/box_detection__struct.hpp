// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from gp7_vision_pipeline:msg/BoxDetection.idl
// generated code does not contain a copyright notice

#ifndef GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__STRUCT_HPP_
#define GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__gp7_vision_pipeline__msg__BoxDetection __attribute__((deprecated))
#else
# define DEPRECATED__gp7_vision_pipeline__msg__BoxDetection __declspec(deprecated)
#endif

namespace gp7_vision_pipeline
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct BoxDetection_
{
  using Type = BoxDetection_<ContainerAllocator>;

  explicit BoxDetection_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->class_name = "";
      this->confidence = 0.0f;
      this->x_min = 0l;
      this->y_min = 0l;
      this->x_max = 0l;
      this->y_max = 0l;
      this->center_x = 0l;
      this->center_y = 0l;
      this->width_px = 0l;
      this->height_px = 0l;
      this->distance_m = 0.0f;
    }
  }

  explicit BoxDetection_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    class_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->class_name = "";
      this->confidence = 0.0f;
      this->x_min = 0l;
      this->y_min = 0l;
      this->x_max = 0l;
      this->y_max = 0l;
      this->center_x = 0l;
      this->center_y = 0l;
      this->width_px = 0l;
      this->height_px = 0l;
      this->distance_m = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _class_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _class_name_type class_name;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _x_min_type =
    int32_t;
  _x_min_type x_min;
  using _y_min_type =
    int32_t;
  _y_min_type y_min;
  using _x_max_type =
    int32_t;
  _x_max_type x_max;
  using _y_max_type =
    int32_t;
  _y_max_type y_max;
  using _center_x_type =
    int32_t;
  _center_x_type center_x;
  using _center_y_type =
    int32_t;
  _center_y_type center_y;
  using _width_px_type =
    int32_t;
  _width_px_type width_px;
  using _height_px_type =
    int32_t;
  _height_px_type height_px;
  using _distance_m_type =
    float;
  _distance_m_type distance_m;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__class_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->class_name = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__x_min(
    const int32_t & _arg)
  {
    this->x_min = _arg;
    return *this;
  }
  Type & set__y_min(
    const int32_t & _arg)
  {
    this->y_min = _arg;
    return *this;
  }
  Type & set__x_max(
    const int32_t & _arg)
  {
    this->x_max = _arg;
    return *this;
  }
  Type & set__y_max(
    const int32_t & _arg)
  {
    this->y_max = _arg;
    return *this;
  }
  Type & set__center_x(
    const int32_t & _arg)
  {
    this->center_x = _arg;
    return *this;
  }
  Type & set__center_y(
    const int32_t & _arg)
  {
    this->center_y = _arg;
    return *this;
  }
  Type & set__width_px(
    const int32_t & _arg)
  {
    this->width_px = _arg;
    return *this;
  }
  Type & set__height_px(
    const int32_t & _arg)
  {
    this->height_px = _arg;
    return *this;
  }
  Type & set__distance_m(
    const float & _arg)
  {
    this->distance_m = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator> *;
  using ConstRawPtr =
    const gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__gp7_vision_pipeline__msg__BoxDetection
    std::shared_ptr<gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__gp7_vision_pipeline__msg__BoxDetection
    std::shared_ptr<gp7_vision_pipeline::msg::BoxDetection_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const BoxDetection_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->class_name != other.class_name) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->x_min != other.x_min) {
      return false;
    }
    if (this->y_min != other.y_min) {
      return false;
    }
    if (this->x_max != other.x_max) {
      return false;
    }
    if (this->y_max != other.y_max) {
      return false;
    }
    if (this->center_x != other.center_x) {
      return false;
    }
    if (this->center_y != other.center_y) {
      return false;
    }
    if (this->width_px != other.width_px) {
      return false;
    }
    if (this->height_px != other.height_px) {
      return false;
    }
    if (this->distance_m != other.distance_m) {
      return false;
    }
    return true;
  }
  bool operator!=(const BoxDetection_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct BoxDetection_

// alias to use template instance with default allocator
using BoxDetection =
  gp7_vision_pipeline::msg::BoxDetection_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace gp7_vision_pipeline

#endif  // GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__STRUCT_HPP_
