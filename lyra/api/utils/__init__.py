def success_message(success, **kwargs):
  message = {'success': success}

  for kwarg in kwargs:
    message[kwarg] = kwargs[kwarg]

  return message