#  Project dangling-journal is developed by "Fahad Ahammed" on 11/12/19, 5:36 PM.
#
#  Last modified at 11/12/19, 5:34 PM.
#
#  Github: fahadahammed
#  Email: obak.krondon@gmail.com
#
#  Copyright (c) 2019. All rights reserved.

from DanglingJournal import app

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
