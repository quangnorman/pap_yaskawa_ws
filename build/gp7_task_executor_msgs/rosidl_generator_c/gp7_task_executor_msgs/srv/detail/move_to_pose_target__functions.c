// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from gp7_task_executor_msgs:srv/MoveToPoseTarget.idl
// generated code does not contain a copyright notice
#include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__init(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * msg)
{
  if (!msg) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__fini(msg);
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__init(&msg->frame_id)) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__fini(msg);
    return false;
  }
  // execute
  return true;
}

void
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__fini(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * msg)
{
  if (!msg) {
    return;
  }
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // frame_id
  rosidl_runtime_c__String__fini(&msg->frame_id);
  // execute
}

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__are_equal(const gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * lhs, const gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->frame_id), &(rhs->frame_id)))
  {
    return false;
  }
  // execute
  if (lhs->execute != rhs->execute) {
    return false;
  }
  return true;
}

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__copy(
  const gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * input,
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__copy(
      &(input->frame_id), &(output->frame_id)))
  {
    return false;
  }
  // execute
  output->execute = input->execute;
  return true;
}

gp7_task_executor_msgs__srv__MoveToPoseTarget_Request *
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * msg = (gp7_task_executor_msgs__srv__MoveToPoseTarget_Request *)allocator.allocate(sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request));
  bool success = gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__destroy(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__init(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * data = NULL;

  if (size) {
    data = (gp7_task_executor_msgs__srv__MoveToPoseTarget_Request *)allocator.zero_allocate(size, sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__fini(&data[i - 1]);
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
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__fini(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence * array)
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
      gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__fini(&array->data[i]);
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

gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence *
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence * array = (gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence *)allocator.allocate(sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__destroy(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__are_equal(const gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence * lhs, const gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence__copy(
  const gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence * input,
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Request * data =
      (gp7_task_executor_msgs__srv__MoveToPoseTarget_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!gp7_task_executor_msgs__srv__MoveToPoseTarget_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__init(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__fini(msg);
    return false;
  }
  return true;
}

void
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__fini(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__are_equal(const gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * lhs, const gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__copy(
  const gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * input,
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

gp7_task_executor_msgs__srv__MoveToPoseTarget_Response *
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * msg = (gp7_task_executor_msgs__srv__MoveToPoseTarget_Response *)allocator.allocate(sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response));
  bool success = gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__destroy(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__init(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * data = NULL;

  if (size) {
    data = (gp7_task_executor_msgs__srv__MoveToPoseTarget_Response *)allocator.zero_allocate(size, sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__fini(&data[i - 1]);
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
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__fini(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence * array)
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
      gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__fini(&array->data[i]);
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

gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence *
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence * array = (gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence *)allocator.allocate(sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__destroy(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__are_equal(const gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence * lhs, const gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence__copy(
  const gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence * input,
  gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(gp7_task_executor_msgs__srv__MoveToPoseTarget_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    gp7_task_executor_msgs__srv__MoveToPoseTarget_Response * data =
      (gp7_task_executor_msgs__srv__MoveToPoseTarget_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!gp7_task_executor_msgs__srv__MoveToPoseTarget_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
