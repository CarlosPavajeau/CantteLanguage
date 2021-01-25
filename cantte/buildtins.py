from typing import cast, Dict
from cantte.object import Builtin, Error, Integer, Object, String


_WRONG_NUMBER_OF_ARGS = 'Wrong number of arguments. {} received, {} expected'
_UNSUPPORTED_ARGUMENT_TYPE = 'Argument of type \'{}\' is not supported'


def size(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
    elif type(args[0]) == String:
        argument = cast(String, args[0])

        return Integer(len(argument.value))
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(args[0].type().name))


BUILTINS: Dict[str, Builtin] = {
    'size': Builtin(function=size),
}
