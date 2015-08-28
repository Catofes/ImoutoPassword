# ImoutoPassword
A tool to generate and store password.

version 0.0.1

##Required
Python 3

##Install

sudo python setup.py install

##Usage

ipw -h

##TODO

A LOT

- IFrame version(chrome extension)
- Sync
- Interaction Mode
- User-define Type
- Daemon Mode
- GUI
- Android

###开发者使用

####密码储存方案


    class Password():
        def __init__(self, id=0, user_id=0, mark="", version=0, length=16, url="", intro="", type="def", structure_version=1,
                     update_time=0, encrypt=False, need_update=False, available=True, special=False, sync_code=""):
            self.id = id
            self.user_id = user_id
            self.mark = mark
            self.version = version
            self.length = length
            self.url = url
            self.intro = intro
            self.type = type
            self.structure_version = structure_version
            self.encrypt = encrypt
            self.update_time = time.time()
            if update_time != 0:
                self.update_time = update_time
            self.need_update = need_update
            self.available = available
            self.special = special
            self.sync_code = sync_code


- id: 密码储存结构的唯一标识。应为不重复的整数。
- mark: 用于生成密码的字段。应为字符串且不应为空）
- version: 用于区分同一个mark下不同的密码，即对于同一个mark可以有很多个版本。同一组相同mark的密码此字段应该不同。不同版本生成不同的密码。
- length: 生成密码长度，密码长度范围应该为8-32个字符。
- url: 用于记录生成此密码的网址信息。仅用于搜索，可以为空。应为字符串
- intro: 用于储存密码的额外信息，例如网站名称，用户名等。仅用于搜索，可以为空，应为字符串。
- type: 用于记录生成密码的类型，和password_type中的处理方法应该一一对应。
- available: 用于删除记录。标记为False即表明记录无效。
- encrypt: True表明该记录加密。现未实现
- structure_version: 表明该记录结构版本，用于向后兼容。
- special: 用于区分一些特殊记录。标记为True表示为特殊记录，详见下述说明。
- need_update: 用于当用户更新记忆密码时提醒用户密码变动的字段。现并未实现。
- user_id： 用于区分用户的唯一标识。应为不重复的整数。在同步时使用。
- update_time: 更新时间戳，应该为浮点数。同步时使用。
- sync_code: 检验记录正确与否以及同步标记。同步中使用。

####密码生成方案：

- 获取主要密码 记作 MPW(master password)
- 获取要生成密码的mark,version,type,length
- 获取配置文件中的盐 salt
- 生成密码 `password = sha512(sha512(MPW + mark + str(version) + salt)+"ImoutoPassword")`
- 应用密码类型。详见下述说明 `password = change_type(password,type)`

####密码类型：

密码类型表示为一个字典：

            "def": {
                "name": "Default",
                "start_with": "",
                "mapping": {
                    "a": "A",
                    "c": "C",
                    "e": "E"
                },
                "regexp": [
                    {
                        "reg": "[A-Z]",
                        "add_at_head": "I",
                        "add_at_end": ""
                    },
                    {
                        "reg": "[a-z]",
                        "add_at_head": "i",
                        "add_at_end": ""
                    },
                    {
                        "reg": "[0-9]",
                        "add_at_head": "",
                        "add_at_end": "1",
                    },
                ],
                "completion": ""
            }

该字典的key `def`即为该密码类型的名字，也是密码储存中type储存的数据。

应用密码类型步骤：

- 获取先前生成的sha512数据password。应为16进制表述的字符串。获取要生成密码的长度length。
- `password = start_with + password`
- 循环字典mapping，将key替换为value。
- `password = password + completion`
- 截取password到length
- 循环regexp, 进行如下处理
  - 搜索正则表达式reg（re.search)。如果匹配继续，否则
  - `password = add_at_head + password`
  - 截取password到length
  - `password = password + add_at_end`
  - 截取password到length(从后截取）
  