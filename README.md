# py-cgmail
A module that leverages pyzmail to parse email messages into json and parses urls out of the message body

# Installation

## Ubuntu
  ```bash
  $ sudo apt-get install -y python-dev python-pip libxml2-dev libxslt1-dev libxml2
  $ pip install --upgrade lxml
  $ pip install cssselect
  $ pip install git+https://github.com/csirtgadgets/py-cifsdk git+https://github.com/csirtgadgets/py-cgmail
  ```

# Examples
```
$ cgmail -h
$ cgmail-cif -h
```

# Support and Documentation

You can also look for information at the [GitHub repo](https://github.com/csirtgadgets/py-cgmail).

# License and Copyright

Copyright (C) 2015 [the CSIRT Gadgets Foundation](http://csirtgadgets.org)

Free use of this software is granted under the terms of the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html) (LGPL v3.0). For details see the file ``LICENSE`` included with the distribution.
