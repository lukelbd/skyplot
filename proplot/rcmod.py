#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# This configures the global working environment
"""
See: https://matplotlib.org/users/customizing.html
Here's a quick list of rcParam categories:
    "lines", "patch", "hatch", "legend"
    "font", "text", "mathtext"
        includes usetex for making all matplotlib fonts latex
        and includes settings options for mathmode math, e.g. sf=sans
    "axes", "figure"
        includes tons of options
    "date", "xtick", "ytick", "grid"
        includes autoformatter
    "contour", "image"
        include lut for size of colormap table
    "boxplot", "errorbar", "hist", "scatter"
    "path", "savefig", "ps", "tk", "pdf", "svg"
    "debug", "keymap", "examples"
    "animation"

Warning: If you try to modify the dictionaries associated with the module
*directly*, the autoreload ipython magic will reload every time! Cannot do this.

Notes
-----
* Note the figure settings are used when printing interactively or just making
    the figure object, but the savefig ones are used when calling savefig.
* Note that if *autoreload* is triggered/global defauls are reset, it seems that
    any options set with InlineBackend in ipython are ***ignored***. But if you query
    settings, options still present -- you just need to call nbsetup again.
* Problem is the settings in rcParams are scattershot and missing some important
    ones we want, but should use it when we can; options won't be rescinded in future versions
* Currently features that can't be rcParam'ed are *gridminor* properties, the
    *cgrid* idea (lines between colorbar colors), the continent/coastlines/lonlatlines
    settings, and some legend settings.

Todo
-----
* Change default background axes color to 0072B2, from seaborn colorblind, just
    a bit darker than figure background; is nice.
* Expand idea of default 'color', 'linewidth', whatever and create more
    dictionaries with defaults settings, then update them. No more hardcoded values
    in the main text below.
"""
#------------------------------------------------------------------------------#
# First just make sure some dependencies are loaded
import re
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from . import colortools
from . import utils
from matplotlib import rcParams, style
# Will add our own dictionary to the top-level matplotlib module, to go
# alongside rcParams
# Default settings
# List of linked settings
rcGlobals = {
    # Apply these ones to list of rcParams
    'color' :     'k',
    'facecolor':  'w',
    'small':      8,
    'large':      9,
    'linewidth':  0.6,
    'bottom':     True,
    'top':        False,
    'left':       True,
    'right':      False,
    'ticklen':    4.0,
    'tickpad':    2.0,
    'inout' :     'out',
    'fontname':   'DejaVu Sans', # simple alias
    # Special ones
    'tickratio':  0.5, # ratio of major-to-minor tick size
    'minorwidth': 0.8, # ratio of major-to-minor tick width
    }
rcGlobals_children = {
    # Most important ones, expect these to be used a lot
    'color':      ['axes.labelcolor', 'axes.edgecolor', 'xtick.color', 'ytick.color'], # change the 'color' of an axes
    'facecolor':  ['axes.facecolor'], # simple alias
    'small':      ['font.size', 'xtick.labelsize', 'ytick.labelsize', 'axes.labelsize', 'legend.fontsize'], # the 'small' fonts
    'large':      ['abc.fontsize', 'figure.titlesize', 'axes.titlesize'], # the 'large' fonts
    'linewidth':  ['axes.linewidth', 'grid.linewidth', 'xtick.major.width', 'ytick.major.width'], # gridline widths same as tick widths
    'fontname':   ['font.sans-serif'],
    # Less important ones
    'bottom':     ['xtick.major.bottom',  'xtick.minor.bottom'], # major and minor ticks should always be in the same place
    'top':        ['xtick.major.top',     'xtick.minor.top'],
    'left':       ['ytick.major.left',    'ytick.minor.left'],
    'right':      ['ytick.major.right',   'ytick.minor.right'],
    'ticklen' :   ['xtick.major.size',    'ytick.major.size'],
    'inout':      ['xtick.direction',     'ytick.direction'],
    'tickpad':    ['xtick.major.pad', 'xtick.minor.pad', 'ytick.major.pad', 'ytick.minor.pad'],
    }
# Settings that apply to just one thing, and are
# already implemented by matplotlib
rcDefaults = {
    'figure.dpi':              90, # save ipython notebook space
    'figure.facecolor':        (0.95,0.95,0.95,1),
    'figure.max_open_warning': 0,
    'figure.autolayout':       False,
    'figure.titleweight':      'bold',
    'savefig.facecolor':       (1,1,1,1),
    'savefig.transparent':     True,
    'savefig.dpi':             300,
    'savefig.pad_inches':      0,
    'savefig.directory':       '',
    'savefig.bbox':            'standard',
    'savefig.format':          'pdf',
    'axes.facecolor':          (1,1,1,1),
    'axes.xmargin':            0,
    'axes.ymargin':            0.05,
    'axes.titleweight':        'normal',
    'axes.labelweight':        'normal',
    'axes.grid':               True,
    'axes.labelpad':           3.0,
    'axes.titlepad':           3.0,
    'axes.axisbelow':          False, # for ticks/gridlines *above* patches, *below* lines, use 'lines'
    'xtick.minor.visible' :    True,
    'ytick.minor.visible' :    True,
    'grid.color':              'k',
    'grid.alpha':              0.1,
    'grid.linestyle':          '-',
    'grid.linewidth':          0.6, # a bit thinner
    'font.family':             'sans-serif',
    'font.sans-serif':         'DejaVu Sans',
    'mathtext.default':        'regular', # no italics
    'mathtext.bf' :            'sans:bold',
    'mathtext.it' :            'sans:it',
    'text.latex.preamble':      r'\usepackage{cmbright}', # https://stackoverflow.com/a/16345065/4970632
    'image.cmap':              'sunset',
    'image.lut':               256,
    'patch.facecolor':         'C0',
    'patch.edgecolor':         'k',
    'patch.linewidth':         1.0,
    'hatch.color':             'k',
    'hatch.linewidth':         1.0,
    'markers.fillstyle':       'full',
    'scatter.marker':          'o',
    'lines.linewidth' :        1.3,
    'lines.color' :            'C0',
    'lines.markeredgewidth' :  0,
    'lines.markersize' :       3.0,
    'lines.dash_joinstyle' :   'miter',
    'lines.dash_capstyle' :    'projecting',
    'lines.solid_joinstyle' :  'miter', # joinstyle opts= miter, round, bevel
    'lines.solid_capstyle' :   'projecting', # capstyle opts= butt, round, projecting
    'legend.fancybox' :        False,
    'legend.frameon' :         False,
    'legend.labelspacing' :    0.5,
    'legend.handletextpad' :   0.5,
    'legend.handlelength' :    1.5,
    'legend.columnspacing' :   1,
    'legend.facecolor' :       'w',
    'legend.numpoints' :       1,
    'legend.borderpad' :       0.5,
    'legend.borderaxespad' :   0,
    }
# Special settings, should be thought of as extension of rcParams
rcSpecial = {
    # These ones just need to be present, will get reset by globals
    'abc.fontsize':          rcGlobals['large'],
    'gridminor.linewidth':   rcGlobals['linewidth']*rcGlobals['minorwidth'],
    # The rest can be applied as-is
    'axes.facehatch':        None, # optionally apply background hatching
    'abc.weight':            'bold',
    'gridminor.color':       'k',
    'gridminor.alpha':       0.1,
    'gridminor.linestyle':   '-',
    'land.linewidth':        0, # no boundary for patch object
    'land.color':            'k',
    'ocean.linewidth':       0, # no boundary for patch object
    'ocean.color':           'w',
    'coastline.linewidth' :  1.0,
    'lonlatlines.linewidth': 1.0,
    # 'lonlatlines.linestyle': ':',
    'lonlatlines.linestyle': '--',
    'lonlatlines.alpha':     0.4,
    'lonlatlines.color':     'k',
    'subplots.title':        0.1, # extra space for title/suptitle
    'subplots.inner':        0.2, # just have ticks, no labeels
    'subplots.legend':       0.25, # default legend space (bottom of figure)
    'subplots.cbar':         0.17, # default colorbar width
    'subplots.ylab':         0.7, # default space wherever we expect tick and axis labels (a bit large if axis has no negative numbers/minus sign tick labels)
    'subplots.xlab':         0.55, # for horizontal text should have more space
    'subplots.nolab':        0.15, # only ticks
    }
# Generate list of categories
rc_categories = {
    re.sub('\..*$', '', name) for name in rcParams.keys()
    }

#------------------------------------------------------------------------------#
# Contextual settings tool
# Using this in day-to-day plotting is annoying and unnecessary, so we abstract
# that away by permitting axes-specific changes requested by .format() input
#------------------------------------------------------------------------------#
class rc_context(object):
    """
    Context object.
    """
    def __init__(self, ax, *args, **kwargs):
        """
        Save user input.
        """
        # Parse input and detect if anything changed (to save time, since in the
        # vact majority of the time, when this is called by format(), we are
        # not going to change any settings)
        for arg in args:
            if not isinstance(arg, dict):
                raise ValueError('rc_context() only accepts dictionary args and kwarg pairs.')
            kwargs.update(arg)
        if not kwargs:
            self._nochange = True
        else:
            self._nochange = False
            self._kwargs = kwargs
            self._special = rc._rcSpecial.copy()
            self._rcparams = rcParams.copy()
            self._ax = ax

    def __enter__(self):
        """
        Apply them, then update all figures.
        """
        if not self._nochange:
            for key,value in self._kwargs.items():
                rc[key] = value # applies globally linked and individual settings

    def __exit__(self, _type, _value, _traceback):
        """
        Return to previous state.
        """
        if not self._nochange:
            for key,value in {**self._rcparams, **self._special}.items():
                rc[key] = value

#-------------------------------------------------------------------------------
# Contextual settings management
# Adapted from seaborn; see: https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py
#-------------------------------------------------------------------------------
class AttributeDict(dict):
    """
    Dictionary elements are attributes too.
    """
    def __getattr__(self, attr): # invoked only if __getattribute__ fails
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value

class rc_configurator(object):
    """
    Abstract class for handling settings.
    """
    def reset(self):
        # Alias to refresh settings
        self.__init__()

    def __init__(self):
        # Note rcdefaults() changes the backend! Inline plotting will fail for
        # rest of notebook session if you call rcdefaults before drawing a figure!
        # After first figure made, backend property is 'sticky', never changes!
        # See: https://stackoverflow.com/a/48322150/4970632
        # First initialize matplotlib
        style.use('default') # mpl.style does not change the backend
        # Add simple attributes to rcParams
        self._rcSpecial = rcSpecial.copy() # *must* be separated from module
        self._rcGlobals = rcGlobals.copy()
        for key,value in rcDefaults.items():
            rcParams[key] = value
        # Apply linked attributes to rcParams
        # The __setitem__ method takes care of details
        self['cycle'] = 'colorblind' # default cycler
        for key,value in self._rcGlobals.items():
            self[key] = value
        # Test if module is in its initial state
        self._init = True

    def __getitem__(self, key):
        # Can get a whole bunch of different things
        # Get full dictionary
        if not key:
            return {**rcParams, **self._rcSpecial}
        # Get a global linked value
        if key in self._rcGlobals:
            return self._rcGlobals[key]
        # Get dictionary of sub-categories
        # Allow access to dictionary contents through attributes
        # NOTE: Try to iterate through dictionary only *once* (could do
        # key in <blank> tests instead of first if statements, but that
        # would often mean two iterations over almost entire dictionary)
        params = AttributeDict()
        for i,d in enumerate((rcParams, self._rcSpecial)):
            for category,value in d.items():
                if re.match(f'^{key}$', category):
                    return d[key]
                elif re.search(f'^{key}\.', category):
                    subcategory = re.sub(f'^{key}.', '', category)
                    if subcategory and '.' not in subcategory:
                        params[subcategory] = d[category]
        if not params:
            raise ValueError(f'Invalid key "{key}".')
        return params

    def __setitem__(self, key, value):
        # Detect aliases
        alias = {alias for alias,names in rcGlobals_children.items() if key in names}
        if len(alias)!=0:
            key = alias.pop() # use
        # First the special cycler
        # NOTE: Generally if user uses 'C0', et cetera, assume they want to
        # refer to the *default* cycler colors; so first reset
        if key=='cycle':
            if isinstance(value, str) or utils.isnumber(value):
                value = value,
            colors = colortools.colors('colorblind')
            self['axes.prop_cycle'] = cycler('color', colors)
            colors = colortools.colors(*value)
            self['axes.prop_cycle'] = cycler('color', colors)
            figs = list(map(plt.figure, plt.get_fignums()))
            for fig in figs:
                for ax in fig.axes:
                    ax.set_prop_cycle(cycler('color', colors))
        # Apply global settings
        elif key in self._rcGlobals:
            self._rcGlobals[key] = value
            # First smarter controls on minor tick length
            if key in ('ticklen','tickratio'):
                if key=='tickratio':
                    ticklen = self._rcGlobals['ticklen']
                    ratio = value
                else:
                    ticklen = value
                    ratio = self._rcGlobals['tickratio']
                rcParams['xtick.minor.size'] = ticklen*ratio
                rcParams['ytick.minor.size'] = ticklen*ratio
            # And on tick width
            if key in ('linewidth','minorwidth'):
                if key=='linewidth':
                    tickwidth = value
                    ratio = self._rcGlobals['minorwidth']
                else:
                    tickwidth = self._rcGlobals['linewidth']
                    ratio = value
                rcParams['xtick.minor.width'] = tickwidth*ratio
                rcParams['ytick.minor.width'] = tickwidth*ratio
                self._rcSpecial['gridminor.linewidth'] = tickwidth*ratio
            # Finally the special settings that correspond to a list of values
            for name in rcGlobals_children.get(key,[]):
                if name in rcParams:
                    rcParams[name] = value
                elif name in self._rcSpecial:
                    self._rcSpecial[name] = value
                else:
                    raise ValueError(f'Invalid key "{name}".')
        # Directly modify single parameter
        elif not isinstance(value, dict):
            if key in rcParams:
                rcParams[key] = value
            elif key in self._rcSpecial:
                self._rcSpecial[key] = value
            else:
                raise ValueError(f'Invalid key "{key}".')
        # Optionally pass a dictionary to modify a bunch of stuff at once
        else:
            kwargs = value
            for name,value in kwargs.items():
                name = f'{key}.{name}'
                if name in rcParams:
                    rcParams[name] = value
                elif name in self._rcSpecial:
                    self._rcSpecial[name] = value
                else:
                    raise ValueError(f'Invalid key "{name}" for parameter "{key}".')
        self._init = False # no longer in initial state

    def __getattribute__(self, attr):
        # Alias to getitem
        if attr.startswith('_') or attr=='reset':
            return super().__getattribute__(attr)
        else:
            return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        # Alias to setitem
        if attr.startswith('_') or attr=='reset':
            super().__setattr__(attr, value)
        else:
            self.__setitem__(attr, value)

    def __repr__(self):
        # Nice string representation
        length = 1 + max(len(key) for key in self._rcGlobals.keys())
        header = 'linked properties'
        header = header + '\n' + '-'*len(header) + '\n'
        header = ''
        string = header + '\n'.join(f'{key}: {" "*(length-len(key))}{value}'
                                    for key,value in self._rcGlobals.items())
        return string

    def __str__(self):
        return self.__repr__()

# Instantiate object
rc = rc_configurator()
