# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2022/5/11 10:25'


class SqliteBasic:

    def __init__(self, sql_dict, conn, cursor):
        """操作sqlite数据库的基类"""
        self.sql_dict = sql_dict
        self.conn = conn
        self.cursor = cursor

    def insert(self, mapping_obj):
        field_str = ", ".join(mapping_obj._fields[1:])
        value_placeholder = ', '.join('?' * (len(mapping_obj._fields) - 1))
        sql = self.sql_dict.get('insert') + f'({field_str}) values ({value_placeholder})'
        self.cursor.execute(sql, mapping_obj[1:])
        self.conn.commit()

    def delete(self, obj_id):
        sql = self.sql_dict.get('delete')
        self.cursor.execute(sql, (obj_id, ))
        self.conn.commit()

    def update_selective(self, mapping_obj):
        sql = self.sql_dict.get('update_selective')
        param = list()
        update_sql = list()
        # 取出主键
        primary_key = mapping_obj._fields[0]
        # 循环字段
        for field, value in mapping_obj._asdict().items():
            # 需要更新的是有值的且非主键
            if value is not None and field != primary_key:
                update_sql.append(f'{field} = ?')
                param.append(value)
        if update_sql:
            # 主键拼在最后作为条件
            sql += ",".join(update_sql) + f' where {primary_key} = ?'
            param.append(mapping_obj[0])
            self.cursor.execute(sql, param)
            self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
