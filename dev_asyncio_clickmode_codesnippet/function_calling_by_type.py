"""
Approach 2

script: function_calling_by_type.py

Make some of the Click Mode Function which support Click Mode as Async and then change the logic during function innovation to use Normal or Awaited Function Calling.

I think this is - Simon Willison's await_me_maybe  which can transparently handle both sync and async callbacks



# Handle both sync and async transparently
await await_me_maybe_with_args(func, x, y)

# This is the simple code
if asyncio.iscoroutinefunction(func):
    await func(x, y)
else:
    func(x, y)

"""


import inspect
import asyncio

async def async_function():
    return "I'm async!"

def normal_function():
    return "I'm normal!"

async def call_function_appropriately(func):
    if inspect.iscoroutinefunction(func):
        print(f"{func.__name__} is async")
        result = await func()
    else:
        print(f"{func.__name__} is normal")
        result = func()
    return result

# Usage
async def main():
    result1 = await call_function_appropriately(async_function)
    result2 = await call_function_appropriately(normal_function)
    print(result1)  # "I'm async!"
    print(result2)  # "I'm normal!"


if __name__ == "__main__":   
    asyncio.run(main())
