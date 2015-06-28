import PIL.Image    # The fundamental PIL library module.
import Win32IconImagePlugin     # Necessary for PIL to properly read any  transparency in .ICO files.

import wx

#------------------------------------------------------------------------------

def BitmapFromFile( imgFilename ) :
    """ The following PIL image conversion must first go to a wx.Image.
    The wx.Image is always finally converted to a wx.Bitmap regardless of whether or not
    there is any image transparency information to be handled.
    This is because only a wxBitmap can be directly displayed - a wxImage can't !

    The module Win32IconImagePlugin.py must be imported to get PIL to properly read
    paletted images with a mask (binary valued transparency). All .ICO and some .PNG files
    may have paletted image data with mask transparency. See:

    Win32IconImagePlugin - Alternate PIL plugin for dealing with Microsoft .ico files.
    http://code.google.com/p/casadebender/wiki/Win32IconImagePlugin
    """
    pilImg = PIL.Image.open( imgFilename )

    # The following is equivalent to "wxImg = wx.EmptyImage( pilImg.size[0], pilImg.size[1] )".
    wxImg = wx.EmptyImage( *pilImg.size )   # Always created with no transparency plane.

    # Determine if the image file has any inherent transparency.
    pilMode = pilImg.mode     # Will usually be either "RGB" or "RGBA", but may be others.
    pilHasAlpha = pilImg.mode[-1] == 'A'
    if pilHasAlpha :

        # First extract just the RGB data from the data string and insert it into wx.Image .
        pilRgbStr = pilImg.convert( 'RGB').tostring()
        wxImg.SetData( pilRgbStr )

        # To convert to a wx.Image with alpha the pilImg mode needs to be "RGBA".
        # So, add an alpha layer even if the original file image doesn't have any transparency info.
        # If the file image doesn't have any transparency, the resulting wx.Image (and, finally, the wx.Bitmap)
        # will be 100% opaque just like the file image.
        pilImgStr = pilImg.convert( 'RGBA' ).tostring()    # Harmless if original image mode is already "RGBA".

        # Now, extract just the alpha data and insert it.
        pilAlphaStr = pilImgStr[3::4]    # start at byte index 3 with a stride (byte skip) of 4.
        wxImg.SetAlphaData( pilAlphaStr )

    #end if

    wxBmap = wxImg.ConvertToBitmap()     # Equivalent result:   wxBmap = wx.BitmapFromImage( wxImg )
    return wxBmap

#end def
