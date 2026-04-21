// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from gp7_task_executor_msgs:srv/MoveToPoseTarget.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__STRUCT_HPP_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__gp7_task_executor_msgs__srv__MoveToPoseTarget_Request __attribute__((deprecated))
#else
# define DEPRECATED__gp7_task_executor_msgs__srv__MoveToPoseTarget_Request __declspec(deprecated)
#endif

namespace gp7_task_executor_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveToPoseTarget_Request_
{
  using Type = MoveToPoseTarget_Request_<ContainerAllocator>;

  explicit MoveToPoseTarget_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->execute = false;
    }
  }

  explicit MoveToPoseTarget_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_alloc, _init),
    frame_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->execute = false;
    }
  }

  // field types and members
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _frame_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _frame_id_type frame_id;
  using _execute_type =
    bool;
  _execute_type execute;

  // setters for named parameter idiom
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__frame_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->frame_id = _arg;
    return *this;
  }
  Type & set__execute(
    const bool & _arg)
  {
    this->execute = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__gp7_task_executor_msgs__srv__MoveToPoseTarget_Request
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__gp7_task_executor_msgs__srv__MoveToPoseTarget_Request
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveToPoseTarget_Request_ & other) const
  {
    if (this->pose != other.pose) {
      return false;
    }
    if (this->frame_id != other.frame_id) {
      return false;
    }
    if (this->execute != other.execute) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveToPoseTarget_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveToPoseTarget_Request_

// alias to use template instance with default allocator
using MoveToPoseTarget_Request =
  gp7_task_executor_msgs::srv::MoveToPoseTarget_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace gp7_task_executor_msgs


#ifndef _WIN32
# define DEPRECATED__gp7_task_executor_msgs__srv__MoveToPoseTarget_Response __attribute__((deprecated))
#else
# define DEPRECATED__gp7_task_executor_msgs__srv__MoveToPoseTarget_Response __declspec(deprecated)
#endif

namespace gp7_task_executor_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveToPoseTarget_Response_
{
  using Type = MoveToPoseTarget_Response_<ContainerAllocator>;

  explicit MoveToPoseTarget_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit MoveToPoseTarget_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__gp7_task_executor_msgs__srv__MoveToPoseTarget_Response
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__gp7_task_executor_msgs__srv__MoveToPoseTarget_Response
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveToPoseTarget_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveToPoseTarget_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveToPoseTarget_Response_

// alias to use template instance with default allocator
using MoveToPoseTarget_Response =
  gp7_task_executor_msgs::srv::MoveToPoseTarget_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace gp7_task_executor_msgs

namespace gp7_task_executor_msgs
{

namespace srv
{

struct MoveToPoseTarget
{
  using Request = gp7_task_executor_msgs::srv::MoveToPoseTarget_Request;
  using Response = gp7_task_executor_msgs::srv::MoveToPoseTarget_Response;
};

}  // namespace srv

}  // namespace gp7_task_executor_msgs

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__STRUCT_HPP_
