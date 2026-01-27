# cppcheck
#
#  Copyright (c) 2026 Mathieu Malaterre <mathieu.malaterre@gmail.com>
#
#  Redistribution and use is allowed according to the terms of the New
#  BSD license.
#  For details see the accompanying COPYING-CMAKE-SCRIPTS file.
#

find_program(CPPCHECK_EXECUTABLE
  cppcheck
  )

mark_as_advanced(
  CPPCHECK_EXECUTABLE
  )
