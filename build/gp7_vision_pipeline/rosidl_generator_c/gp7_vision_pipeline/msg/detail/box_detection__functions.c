// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from gp7_vision_pipeline:msg/BoxDetection.idl
// generated code does not contain a copyright notice
#include "gp7_vision_pipeline/msg/detail/box_detection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `class_name`
#include "rosidl_runtime_c/string_functions.h"

bool
gp7_vision_pipeline__msg__BoxDetection__init(gp7_vision_pipeline__msg__BoxDetection * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    gp7_vision_pipeline__msg__BoxDetection__fini(msg);
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__init(&msg->class_name)) {
    gp7_vision_pipeline__msg__BoxDetection__fini(msg);
    return false;
  }
  // confidence
  // x_min
  // y_min
  // x_max
  // y_max
  // center_x
  // center_y
  // width_px
  // height_px
  // distance_m
  return true;
}

void
gp7_vision_pipeline__msg__BoxDetection__fini(gp7_vision_pipeline__msg__BoxDetection * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // class_name
  rosidl_runtime_c__String__fini(&msg->class_name);
  // confidence
  // x_min
  // y_min
  // x_max
  // y_max
  // center_x
  // center_y
  // width_px
  // height_px
  // distance_m
}

bool
gp7_vision_pipeline__msg__BoxDetection__are_equal(const gp7_vision_pipeline__msg__BoxDetection * lhs, const gp7_vision_pipeline__msg__BoxDetection * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->class_name), &(rhs->class_name)))
  {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // x_min
  if (lhs->x_min != rhs->x_min) {
    return false;
  }
  // y_min
  if (lhs->y_min != rhs->y_min) {
    return false;
  }
  // x_max
  if (lhs->x_max != rhs->x_max) {
    return false;
  }
  // y_max
  if (lhs->y_max != rhs->y_max) {
    return false;
  }
  // center_x
  if (lhs->center_x != rhs->center_x) {
    return false;
  }
  // center_y
  if (lhs->center_y != rhs->center_y) {
    return false;
  }
  // width_px
  if (lhs->width_px != rhs->width_px) {
    return false;
  }
  // height_px
  if (lhs->height_px != rhs->height_px) {
    return false;
  }
  // distance_m
  if (lhs->distance_m != rhs->distance_m) {
    return false;
  }
  return true;
}

bool
gp7_vision_pipeline__msg__BoxDetection__copy(
  const gp7_vision_pipeline__msg__BoxDetection * input,
  gp7_vision_pipeline__msg__BoxDetection * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__copy(
      &(input->class_name), &(output->class_name)))
  {
    return false;
  }
  // confidence
  output->confidence = input->confidence;
  // x_min
  output->x_min = input->x_min;
  // y_min
  output->y_min = input->y_min;
  // x_max
  output->x_max = input->x_max;
  // y_max
  output->y_max = input->y_max;
  // center_x
  output->center_x = input->center_x;
  // center_y
  output->center_y = input->center_y;
  // width_px
  output->width_px = input->width_px;
  // height_px
  output->height_px = input->height_px;
  // distance_m
  output->distance_m = input->distance_m;
  return true;
}

gp7_vision_pipeline__msg__BoxDetection *
gp7_vision_pipeline__msg__BoxDetection__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_vision_pipeline__msg__BoxDetection * msg = (gp7_vision_pipeline__msg__BoxDetection *)allocator.allocate(sizeof(gp7_vision_pipeline__msg__BoxDetection), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(gp7_vision_pipeline__msg__BoxDetection));
  bool success = gp7_vision_pipeline__msg__BoxDetection__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
gp7_vision_pipeline__msg__BoxDetection__destroy(gp7_vision_pipeline__msg__BoxDetection * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    gp7_vision_pipeline__msg__BoxDetection__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
gp7_vision_pipeline__msg__BoxDetection__Sequence__init(gp7_vision_pipeline__msg__BoxDetection__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_vision_pipeline__msg__BoxDetection * data = NULL;

  if (size) {
    data = (gp7_vision_pipeline__msg__BoxDetection *)allocator.zero_allocate(size, sizeof(gp7_vision_pipeline__msg__BoxDetection), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = gp7_vision_pipeline__msg__BoxDetection__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        gp7_vision_pipeline__msg__BoxDetection__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
gp7_vision_pipeline__msg__BoxDetection__Sequence__fini(gp7_vision_pipeline__msg__BoxDetection__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      gp7_vision_pipeline__msg__BoxDetection__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

gp7_vision_pipeline__msg__BoxDetection__Sequence *
gp7_vision_pipeline__msg__BoxDetection__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_vision_pipeline__msg__BoxDetection__Sequence * array = (gp7_vision_pipeline__msg__BoxDetection__Sequence *)allocator.allocate(sizeof(gp7_vision_pipeline__msg__BoxDetection__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = gp7_vision_pipeline__msg__BoxDetection__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
gp7_vision_pipeline__msg__BoxDetection__Sequence__destroy(gp7_vision_pipeline__msg__BoxDetection__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    gp7_vision_pipeline__msg__BoxDetection__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
gp7_vision_pipeline__msg__BoxDetection__Sequence__are_equal(const gp7_vision_pipeline__msg__BoxDetection__Sequence * lhs, const gp7_vision_pipeline__msg__BoxDetection__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!gp7_vision_pipeline__msg__BoxDetection__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
gp7_vision_pipeline__msg__BoxDetection__Sequence__copy(
  const gp7_vision_pipeline__msg__BoxDetection__Sequence * input,
  gp7_vision_pipeline__msg__BoxDetection__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(gp7_vision_pipeline__msg__BoxDetection);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    gp7_vision_pipeline__msg__BoxDetection * data =
      (gp7_vision_pipeline__msg__BoxDetection *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!gp7_vision_pipeline__msg__BoxDetection__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          gp7_vision_pipeline__msg__BoxDetection__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!gp7_vision_pipeline__msg__BoxDetection__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
