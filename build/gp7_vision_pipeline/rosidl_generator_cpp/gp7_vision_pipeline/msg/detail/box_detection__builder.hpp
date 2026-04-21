// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from gp7_vision_pipeline:msg/BoxDetection.idl
// generated code does not contain a copyright notice

#ifndef GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__BUILDER_HPP_
#define GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "gp7_vision_pipeline/msg/detail/box_detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace gp7_vision_pipeline
{

namespace msg
{

namespace builder
{

class Init_BoxDetection_distance_m
{
public:
  explicit Init_BoxDetection_distance_m(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  ::gp7_vision_pipeline::msg::BoxDetection distance_m(::gp7_vision_pipeline::msg::BoxDetection::_distance_m_type arg)
  {
    msg_.distance_m = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_height_px
{
public:
  explicit Init_BoxDetection_height_px(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_distance_m height_px(::gp7_vision_pipeline::msg::BoxDetection::_height_px_type arg)
  {
    msg_.height_px = std::move(arg);
    return Init_BoxDetection_distance_m(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_width_px
{
public:
  explicit Init_BoxDetection_width_px(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_height_px width_px(::gp7_vision_pipeline::msg::BoxDetection::_width_px_type arg)
  {
    msg_.width_px = std::move(arg);
    return Init_BoxDetection_height_px(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_center_y
{
public:
  explicit Init_BoxDetection_center_y(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_width_px center_y(::gp7_vision_pipeline::msg::BoxDetection::_center_y_type arg)
  {
    msg_.center_y = std::move(arg);
    return Init_BoxDetection_width_px(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_center_x
{
public:
  explicit Init_BoxDetection_center_x(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_center_y center_x(::gp7_vision_pipeline::msg::BoxDetection::_center_x_type arg)
  {
    msg_.center_x = std::move(arg);
    return Init_BoxDetection_center_y(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_y_max
{
public:
  explicit Init_BoxDetection_y_max(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_center_x y_max(::gp7_vision_pipeline::msg::BoxDetection::_y_max_type arg)
  {
    msg_.y_max = std::move(arg);
    return Init_BoxDetection_center_x(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_x_max
{
public:
  explicit Init_BoxDetection_x_max(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_y_max x_max(::gp7_vision_pipeline::msg::BoxDetection::_x_max_type arg)
  {
    msg_.x_max = std::move(arg);
    return Init_BoxDetection_y_max(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_y_min
{
public:
  explicit Init_BoxDetection_y_min(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_x_max y_min(::gp7_vision_pipeline::msg::BoxDetection::_y_min_type arg)
  {
    msg_.y_min = std::move(arg);
    return Init_BoxDetection_x_max(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_x_min
{
public:
  explicit Init_BoxDetection_x_min(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_y_min x_min(::gp7_vision_pipeline::msg::BoxDetection::_x_min_type arg)
  {
    msg_.x_min = std::move(arg);
    return Init_BoxDetection_y_min(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_confidence
{
public:
  explicit Init_BoxDetection_confidence(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_x_min confidence(::gp7_vision_pipeline::msg::BoxDetection::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_BoxDetection_x_min(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_class_name
{
public:
  explicit Init_BoxDetection_class_name(::gp7_vision_pipeline::msg::BoxDetection & msg)
  : msg_(msg)
  {}
  Init_BoxDetection_confidence class_name(::gp7_vision_pipeline::msg::BoxDetection::_class_name_type arg)
  {
    msg_.class_name = std::move(arg);
    return Init_BoxDetection_confidence(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

class Init_BoxDetection_header
{
public:
  Init_BoxDetection_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BoxDetection_class_name header(::gp7_vision_pipeline::msg::BoxDetection::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_BoxDetection_class_name(msg_);
  }

private:
  ::gp7_vision_pipeline::msg::BoxDetection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::gp7_vision_pipeline::msg::BoxDetection>()
{
  return gp7_vision_pipeline::msg::builder::Init_BoxDetection_header();
}

}  // namespace gp7_vision_pipeline

#endif  // GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__BUILDER_HPP_
