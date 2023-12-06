import types

import mymodule


stop_types = [int, float, bool, str, bytes, bytearray, types.NoneType,
              types.BuiltinMethodType, types.BuiltinFunctionType,
              types.FunctionType, types.MethodType, types.MethodWrapperType,
              types.MemberDescriptorType, types.MethodDescriptorType,
              types.WrapperDescriptorType, types.ClassMethodDescriptorType,
              types.GetSetDescriptorType]

container_types = [list, tuple, set, frozenset]

def immortalize_object(obj, stats=False) -> int:
    queue    = [obj]  # A queue for iterative immortalization

    visited  = set()  # A set of visited objects' ids to avoid infinite loops
                      # mymodule.is_immortal() cannot be used to check infinite
                      # loops because certain objects cannot be immortalized,
                      # such as numeric literals, method wrappers, etc.

    count    = 0      # The number of new immortal objects; *may be inaccurate*

    error    = 0      # The number of objects that cannot be immortalized due to
                      # various errors, such as AttributeError, ValueError, etc.

    freqd    = {}     # A dictionary that stores the frequency of object types
                      # that appear in the queue; only used if stats=True

    MAX_OBJS = 1e5    # The cap number of objects that can be checked; used to
                      # to avoid "infinite" loops

    iters    = MAX_OBJS

    while len(queue) > 0 and iters > 0:
        iters -= 1

        ob = queue.pop(0)

        if id(ob) in visited or mymodule.is_immortal(ob):
            continue

        visited.add(id(ob))
        count += mymodule.immortalize(ob)
        otype = type(ob)

        if stats:
            if otype.__name__ in freqd:
                freqd[otype.__name__] += 1
            else:
                freqd[otype.__name__] = 1

        if otype in stop_types:
            continue
        elif otype in container_types:
            queue += [e for e in ob]
        elif isinstance(ob, dict):
            for k, v in ob.items():
                queue.append(k)
                queue.append(v)
        else:
            for name in dir(ob):
                try:
                    attr = getattr(ob, name)
                    queue.append(attr)
                except Exception:
                    error += 1

    return count, error, freqd, len(queue) == 0

