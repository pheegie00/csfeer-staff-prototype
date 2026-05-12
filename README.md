# Repository Coverage



| Name                                                      |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------------------- | -------: | -------: | ------: | --------: |
| core/\_\_init\_\_.py                                      |        0 |        0 |    100% |           |
| core/admin.py                                             |        0 |        0 |    100% |           |
| core/apps.py                                              |        3 |        0 |    100% |           |
| core/models.py                                            |        8 |        0 |    100% |           |
| core/tests.py                                             |        0 |        0 |    100% |           |
| core/views.py                                             |        0 |        0 |    100% |           |
| csfeer/\_\_init\_\_.py                                    |        0 |        0 |    100% |           |
| csfeer/asgi.py                                            |        4 |        4 |      0% |     10-16 |
| csfeer/auth\_backends/\_\_init\_\_.py                     |        5 |        1 |     80% |         7 |
| csfeer/auth\_backends/form\_permissions.py                |       22 |        1 |     95% |        22 |
| csfeer/auth\_backends/oidc\_backend.py                    |       53 |       25 |     53% |45-73, 106-114 |
| csfeer/config.py                                          |       51 |        0 |    100% |           |
| csfeer/context\_processors.py                             |        3 |        0 |    100% |           |
| csfeer/postgresql/base.py                                 |       14 |        3 |     79% |     15-21 |
| csfeer/settings.py                                        |       53 |        0 |    100% |           |
| csfeer/templatetags/\_\_init\_\_.py                       |        0 |        0 |    100% |           |
| csfeer/templatetags/crispy\_forms\_foundation\_field.py   |       57 |       57 |      0% |     6-129 |
| csfeer/urls.py                                            |        8 |        0 |    100% |           |
| csfeer/utils/\_\_init\_\_.py                              |        0 |        0 |    100% |           |
| csfeer/utils/crispy\_components.py                        |       11 |       11 |      0% |      1-31 |
| csfeer/wsgi.py                                            |        4 |        4 |      0% |     10-16 |
| form\_manager/\_\_init\_\_.py                             |        1 |        0 |    100% |           |
| form\_manager/admin.py                                    |       58 |       15 |     74% |43-59, 83-84 |
| form\_manager/api/\_\_init\_\_.py                         |        2 |        0 |    100% |           |
| form\_manager/api/endpoints.py                            |       57 |       32 |     44% |47-52, 57-58, 67, 77-78, 101-117, 136-141, 154-159, 169-174, 183-184 |
| form\_manager/api/schemas.py                              |       19 |        0 |    100% |           |
| form\_manager/apps.py                                     |        5 |        0 |    100% |           |
| form\_manager/constants.py                                |       17 |        0 |    100% |           |
| form\_manager/locking.py                                  |       59 |       13 |     78% |19-20, 36-47, 84-86 |
| form\_manager/management/commands/load\_initial\_forms.py |       34 |        9 |     74% |34, 38-40, 58-73 |
| form\_manager/models/\_\_init\_\_.py                      |        3 |        0 |    100% |           |
| form\_manager/models/fields.py                            |       22 |       13 |     41% |10-14, 18-24, 32 |
| form\_manager/models/forms.py                             |       44 |        0 |    100% |           |
| form\_manager/models/locking.py                           |       10 |        0 |    100% |           |
| form\_manager/schema/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| form\_manager/schema/choices.py                           |       11 |        0 |    100% |           |
| form\_manager/schema/fields.py                            |      232 |       13 |     94% |148-149, 293, 297, 305, 318-322, 347, 390-391 |
| form\_manager/schema/forms/\_\_init\_\_.py                |        6 |        0 |    100% |           |
| form\_manager/schema/forms/base.py                        |       65 |        2 |     97% |   116-117 |
| form\_manager/schema/forms/tribal\_long\_form.py          |       54 |        0 |    100% |           |
| form\_manager/schema/forms/tribal\_plan/\_\_init\_\_.py   |        2 |        0 |    100% |           |
| form\_manager/schema/forms/tribal\_plan/fields.py         |      144 |        5 |     97% |612, 673-679, 688 |
| form\_manager/schema/forms/tribal\_plan/form.py           |       18 |        0 |    100% |           |
| form\_manager/schema/forms/tribal\_plan/texts.py          |       11 |        0 |    100% |           |
| form\_manager/schema/forms/tribal\_short\_form.py         |       40 |        0 |    100% |           |
| form\_manager/schema/forms/utils.py                       |        3 |        0 |    100% |           |
| form\_manager/schema/layout.py                            |      232 |       23 |     90% |30-32, 36-43, 114-122, 385, 409, 439-446 |
| form\_manager/schema/navigation.py                        |       86 |       10 |     88% |53, 65, 78-87 |
| form\_manager/schema/widgets.py                           |       38 |        4 |     89% | 22, 69-72 |
| form\_manager/templatetags/\_\_init\_\_.py                |        0 |        0 |    100% |           |
| form\_manager/templatetags/form\_manager\_tags.py         |       32 |       23 |     28% |15-21, 29-64 |
| form\_manager/urls.py                                     |        3 |        0 |    100% |           |
| form\_manager/utils.py                                    |      127 |       28 |     78% |28-38, 43-46, 51-58, 86, 88, 90, 160-162, 202, 212 |
| form\_manager/views/\_\_init\_\_.py                       |        6 |        0 |    100% |           |
| form\_manager/views/base.py                               |       56 |       26 |     54% |27-28, 31-32, 46-48, 53-55, 59-61, 65, 68-79, 88, 91-92, 95-96, 99-100, 103-113 |
| form\_manager/views/form\_download.py                     |       22 |       12 |     45% |16-19, 22-46 |
| form\_manager/views/form\_edit.py                         |      121 |       16 |     87% |40, 49, 78-79, 82, 85, 105, 158, 162-163, 175-176, 179-180, 184-189 |
| form\_manager/views/form\_finalize.py                     |       46 |        7 |     85% |33-34, 38-43, 56, 60-61 |
| form\_manager/views/form\_review.py                       |       81 |       21 |     74% |37-44, 56-62, 107-108, 111-112, 116-121, 126, 130-131, 140 |
| form\_manager/views/form\_views.py                        |      126 |       62 |     51% |28-36, 47-49, 51-53, 74-78, 84-97, 110-114, 117-118, 123-124, 127-135, 140-148, 153-161, 166-175 |
| organizations/\_\_init\_\_.py                             |        0 |        0 |    100% |           |
| organizations/admin.py                                    |       40 |       18 |     55% |22-24, 30-60 |
| organizations/apps.py                                     |        9 |        0 |    100% |           |
| organizations/models.py                                   |       16 |        0 |    100% |           |
| organizations/signals.py                                  |       14 |        0 |    100% |           |
| organizations/tests.py                                    |        0 |        0 |    100% |           |
| organizations/utils.py                                    |        8 |        1 |     88% |        20 |
| organizations/views.py                                    |        0 |        0 |    100% |           |
| users/\_\_init\_\_.py                                     |        0 |        0 |    100% |           |
| users/admin.py                                            |       18 |        0 |    100% |           |
| users/apps.py                                             |        5 |        0 |    100% |           |
| users/managers.py                                         |       20 |        3 |     85% |16, 32, 34 |
| users/models.py                                           |       21 |        2 |     90% |    23, 38 |
| users/permissions.py                                      |       28 |        0 |    100% |           |
| users/signals.py                                          |       20 |        1 |     95% |        18 |
| users/templatetags/\_\_init\_\_.py                        |        0 |        0 |    100% |           |
| users/templatetags/user\_tags.py                          |       21 |        6 |     71% |17, 22, 27, 32, 37, 42 |
| users/tests.py                                            |        0 |        0 |    100% |           |
| users/utils.py                                            |       17 |        3 |     82% |22, 30, 38 |
| users/views.py                                            |        0 |        0 |    100% |           |
| **TOTAL**                                                 | **2426** |  **474** | **80%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://github.com/focusconsulting/csfeer/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/focusconsulting/csfeer/tree/python-coverage-comment-action-data)

This is the one to use if your repository is private or if you don't want to customize anything.



## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.