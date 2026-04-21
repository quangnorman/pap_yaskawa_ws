// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from gp7_task_executor_msgs:srv/MoveToJointTarget.idl
// generated code does not contain a copyright notice
#include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `joint_names`
#include "rosidl_runtime_c/string_functions.h"
// Member `positions`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__init(gp7_task_executor_msgs__srv__MoveToJointTarget_Request * msg)
{
  if (!msg) {
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__init(&msg->joint_names, 0)) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__fini(msg);
    return false;
  }
  // positions
  if (!rosidl_runtime_c__double__Sequence__init(&msg->positions, 0)) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__fini(msg);
    return false;
  }
  // execute
  return true;
}

void
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__fini(gp7_task_executor_msgs__srv__MoveToJointTarget_Request * msg)
{
  if (!msg) {
    return;
  }
  // joint_names
  rosidl_runtime_c__String__Sequence__fini(&msg->joint_names);
  // positions
  rosidl_runtime_c__double__Sequence__fini(&msg->positions);
  // execute
}

bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__are_equal(const gp7_task_executor_msgs__srv__MoveToJointTarget_Request * lhs, const gp7_task_executor_msgs__srv__MoveToJointTarget_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->joint_names), &(rhs->joint_names)))
  {
    return false;
  }
  // positions
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->positions), &(rhs->positions)))
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
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__copy(
  const gp7_task_executor_msgs__srv__MoveToJointTarget_Request * input,
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->joint_names), &(output->joint_names)))
  {
    return false;
  }
  // positions
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->positions), &(output->positions)))
  {
    return false;
  }
  // execute
  output->execute = input->execute;
  return true;
}

gp7_task_executor_msgs__srv__MoveToJointTarget_Request *
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request * msg = (gp7_task_executor_msgs__srv__MoveToJointTarget_Request *)allocator.allocate(sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request));
  bool success = gp7_task_executor_msgs__srv__MoveToJointTarget_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__destroy(gp7_task_executor_msgs__srv__MoveToJointTarget_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__init(gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request * data = NULL;

  if (size) {
    data = (gp7_task_executor_msgs__srv__MoveToJointTarget_Request *)allocator.zero_allocate(size, sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = gp7_task_executor_msgs__srv__MoveToJointTarget_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        gp7_task_executor_msgs__srv__MoveToJointTarget_Request__fini(&data[i - 1]);
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
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__fini(gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence * array)
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
      gp7_task_executor_msgs__srv__MoveToJointTarget_Request__fini(&array->data[i]);
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

gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence *
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence * array = (gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence *)allocator.allocate(sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__destroy(gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__are_equal(const gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence * lhs, const gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!gp7_task_executor_msgs__srv__MoveToJointTarget_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence__copy(
  const gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence * input,
  gp7_task_executor_msgs__srv__MoveToJointTarget_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    gp7_task_executor_msgs__srv__MoveToJointTarget_Request * data =
      (gp7_task_executor_msgs__srv__MoveToJointTarget_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!gp7_task_executor_msgs__srv__MoveToJointTarget_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          gp7_task_executor_msgs__srv__MoveToJointTarget_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!gp7_task_executor_msgs__srv__MoveToJointTarget_Request__copy(
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
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__init(gp7_task_executor_msgs__srv__MoveToJointTarget_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Response__fini(msg);
    return false;
  }
  return true;
}

void
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__fini(gp7_task_executor_msgs__srv__MoveToJointTarget_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__are_equal(const gp7_task_executor_msgs__srv__MoveToJointTarget_Response * lhs, const gp7_task_executor_msgs__srv__MoveToJointTarget_Response * rhs)
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
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__copy(
  const gp7_task_executor_msgs__srv__MoveToJointTarget_Response * input,
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response * output)
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

gp7_task_executor_msgs__srv__MoveToJointTarget_Response *
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response * msg = (gp7_task_executor_msgs__srv__MoveToJointTarget_Response *)allocator.allocate(sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Response));
  bool success = gp7_task_executor_msgs__srv__MoveToJointTarget_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__destroy(gp7_task_executor_msgs__srv__MoveToJointTarget_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__init(gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response * data = NULL;

  if (size) {
    data = (gp7_task_executor_msgs__srv__MoveToJointTarget_Response *)allocator.zero_allocate(size, sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = gp7_task_executor_msgs__srv__MoveToJointTarget_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        gp7_task_executor_msgs__srv__MoveToJointTarget_Response__fini(&data[i - 1]);
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
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__fini(gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence * array)
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
      gp7_task_executor_msgs__srv__MoveToJointTarget_Response__fini(&array->data[i]);
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

gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence *
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence * array = (gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence *)allocator.allocate(sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__destroy(gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__are_equal(const gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence * lhs, const gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!gp7_task_executor_msgs__srv__MoveToJointTarget_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence__copy(
  const gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence * input,
  gp7_task_executor_msgs__srv__MoveToJointTarget_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(gp7_task_executor_msgs__srv__MoveToJointTarget_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    gp7_task_executor_msgs__srv__MoveToJointTarget_Response * data =
      (gp7_task_executor_msgs__srv__MoveToJointTarget_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!gp7_task_executor_msgs__srv__MoveToJointTarget_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          gp7_task_executor_msgs__srv__MoveToJointTarget_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!gp7_task_executor_msgs__srv__MoveToJointTarget_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
