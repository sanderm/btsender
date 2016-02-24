#!/usr/bin/env python
from distutils.core import setup, Extension
from distutils.command.install_data import install_data

pythonussp = Extension('pythonussp', ['src/obex_main.c',
				      'src/obex_sdp.c',
				      'src/obex_socket.c',
				      'src/obex_wrap.c',],
		       define_macros = [('MAJOR_VERSION', '1'),
					('MINOR_VERSION', '0')],
		       include_dirs = ['/usr/local/include',
				       '/usr/include/python2.4'],
		       libraries = ['openobex', 'bluetooth'],
		       library_dirs = ['/usr/local/lib'],
		       )

class smart_install_data(install_data):
	def run(self):
		#need to change self.install_dir to the library dir
		install_cmd = self.get_finalized_command('install')
		self.install_dir = getattr(install_cmd, 'install_lib')
		return install_data.run(self)

setup(name='BTSender',
      version = '1.1.0',
      description = 'BlueTooth automatic file sender',
      author = 'Arve B/Sander J',
      author_email = 'arveba/sanderj@ifi.uio.no',
      url = 'http://www.uio.no',
      packages = ['BTSender'],
      package_dir = {'BTSender': ''},
      data_files = [('BTSender/files', ['files/klovner.jpg', 'files/klovner2.jpg']),
		    ('BTSender', ['start.sh']),
                    ('BTSender', ['COPYING'])],
      cmdclass = {'install_data': smart_install_data},
      ext_package = 'BTSender',
      ext_modules = [pythonussp],
      )
