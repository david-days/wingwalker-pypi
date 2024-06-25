from setuptools import setup

setup(name='wingwalker',
      version='1.0.0.a1',
      description='Wingwalker Airfoil and Wing Design Tools',
      long_description=read('README.md'),
      keywords="airfoil aeronautics engineering wing selig lednicer 3d-printing",
      author='David C. Days',
      author_email='david.c.days@gmail.com',
      license='mit',
      url="https://github.com/boudinfl/pke",
      install_requires=[
            'requests',
            'importlib-metadata; python_version>="3.12"',
            'pycairo'
      ],
      packages=[
            'wingwalker',
            'tests'
      ],
      include_package_data=True,
      package_data={
            'wingwalker': [
                        'templates/*.tpl'
                  ],
            'tests': [
                        'dat/*.dat',
                        'dat/*.txt'
                  ]
            }
      )
