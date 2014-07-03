import pickle


class CallbackWrapper(object):
    def __init__(self, func, callback):
        self.func = func
        self.callback = callback
    
    def __call__(self, *args, **kwargs):
        value = self.func(*args, **kwargs)
        self.callback(value)
        return value


class FileDict(dict):
    ALTERING_FUNCS = ['update', 'clear', '__setitem__', '__delitem__', 'pop', 'popitem', 'setdefault']

    def __init__(self, filename, *args, **kwargs):
        self.loaded = False
        self.filename = filename
        super(FileDict, self).__init__(*args, **kwargs)

    def __getattribute__(self, item):
        return object.__getattribute__(self, '_get_attribute')(item)

    def _get_attribute(self, item):
        if not object.__getattribute__(self, 'loaded'):
            load_func = object.__getattribute__(self, 'load')
            load_func()

        value = lambda *args, **kwargs: getattr(dict, item)(self, *args, **kwargs)
        if item in object.__getattribute__(self, 'ALTERING_FUNCS'):
            save_func = object.__getattribute__(self, 'save')
            value = CallbackWrapper(value, lambda _: save_func())

        return value

    def load(self):
        try:
            with open(object.__getattribute__(self, 'filename')) as data_file:
                data = pickle.load(data_file)
        except IOError:
            # File does not exist
            pass
        except EOFError:
            # Exists, but no data
            pass
        else:
            # Get the real update function, so we don't trigger a load
            update_func = object.__getattribute__(self, 'update')
            update_func(data)

        self.loaded = True

    def save(self):
        with open(object.__getattribute__(self, 'filename'), 'w') as data_file:
            pickle.dump(self.copy(), data_file)

    __iter__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__iter__'))
    __getitem__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__getitem__'))
    __setitem__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__setitem__'))
    __delitem__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __cmp__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __ge__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __gt__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __eq__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __le__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __lt__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __len__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __contains__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__delitem__'))
    __ne__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__ne__'))
    __repr__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__ne__'))
    __class__ = property(lambda self: object.__getattribute__(self, '_get_attribute')('__class__'))
