# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/1/17 9:33'


# 每个表id生成器字典
table_id_generator_dict = dict()


def generate_id(id_start):
    id_end = id_start
    while True:
        id_count = yield list(range(id_start, id_end))
        id_start = id_end
        id_end += id_count


def get_id(table_name, id_count):
    generator = table_id_generator_dict.get(table_name)
    if generator is None:
        update_id_generator(table_name)
        return get_id(table_name, id_count)
    return generator.send(id_count)


def init_id_generator(get_sqlite_sequence_func):
    # 初始化每个表的id生成器
    sequence_list = get_sqlite_sequence_func()
    for row_data in sequence_list:
        table_sequence = dict(row_data)
        generator = generate_id(table_sequence.get('seq') + 1)
        generator.__next__()
        table_id_generator_dict[table_sequence.get('name')] = generator


def update_id_generator(table_name):
    # 更新只会在表重新创建或清空表时调用，所以id的初始值为1
    generator = generate_id(1)
    generator.__next__()
    table_id_generator_dict[table_name] = generator
