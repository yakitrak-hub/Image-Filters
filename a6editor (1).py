"""
The primary controller module for the Imager application

This module provides all of the image processing operations that are called whenever you 
press a button. Some of these are provided for you and others you are expected to write
on your own.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:    October 20, 2017 (Python 3 Version)

Kartikay Jain kj295
11/15/2017
"""
import a6history


class Editor(a6history.ImageHistory):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of ImageHistory.  That means it inherits all of the methods
    and attributes of that class.  We do that (1) to put all of the image processing
    methods in one easy-to-read place and (2) because we might want to change how we 
    implement the undo functionality later.
    
    This class is broken up into three parts (1) implemented non-hidden methods, (2)
    non-implemented non-hidden methods and (3) hidden methods.  The non-hidden methods
    each correspond to a button press in the main application.  The hidden methods are
    all helper functions.
    
    Each one of the non-hidden functions should edit the most recent image in the
    edit history (which is inherited from ImageHistory).
    """
    
    # PROVIDED ACTIONS (STUDY THESE)
    def invert(self):
        """
        Inverts the current image, replacing each element with its color complement
        """
        current = self.getCurrent()
        for pos in range(current.getLength()):
            rgb = current.getFlatPixel(pos)
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue) # New pixel value
            current.setFlatPixel(pos,rgb)
    
    
    def transpose(self):
        """
        Transposes the current image
        
        Transposing is tricky, as it is hard to remember which values have been changed 
        and which have not.  To simplify the process, we copy the current image and use
        that as a reference.  So we change the current image with setPixel, but read
        (with getPixel) from the copy.
        
        The transposed image will be drawn on the screen immediately afterwards.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,row))
    
    
    def reflectHori(self):
        """
        Reflects the current image around the horizontal middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()//2):
            for row in range(current.getHeight()):
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)
    
    
    def rotateRight(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,\
original.getPixel(original.getHeight()-col-1,row))
    
    
    def rotateLeft(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,\
original.getPixel(col,original.getWidth()-row-1))
    
    
    # ASSIGNMENT METHODS (IMPLEMENT THESE)
    def reflectVert(self):
        """ 
        Reflects the current image around the vertical middle.
        """
        current = self.getCurrent()
        for r in range(current.getHeight()//2):
            for h in range(current.getWidth()):
                k = current.getHeight()-1-r
                current.swapPixels(r,h,k,h)
    
    
    def monochromify(self, sepia):
        """
        Converts the current image to monochrome, using either greyscale or sepia tone.
        
        If `sepia` is False, then this function uses greyscale.  It removes all color 
        from the image by setting the three color components of each pixel to that pixel's 
        overall brightness, defined as 
            
            0.3 * red + 0.6 * green + 0.1 * blue.
        
        If sepia is True, it makes the same computations as before but sets green to
        0.6 * brightness and blue to 0.4 * brightness.
        
        Parameter sepia: Whether to use sepia tone instead of greyscale.
        Precondition: sepia is a bool
        """
        current = self.getCurrent()
        if sepia==True:
            for pos in range(current.getLength()):
                rgb = current.getFlatPixel(pos)
                brightness=0.3*rgb[0] + 0.6*rgb[1] + 0.1*rgb[2]
                red   = rgb[0]
                green = int(0.6 * brightness)
                blue  = int(0.4 * brightness)
                rgb = (red,green,blue) # New pixel value
                current.setFlatPixel(pos,rgb)
        else:
            for pos in range(current.getLength()):
                rgb = current.getFlatPixel(pos)
                brightness=0.3*rgb[0] + 0.6*rgb[1] + 0.1*rgb[2]
                red   = int(brightness)
                green = int(brightness)
                blue  = int(brightness)
                rgb = (red,green,blue)  # New pixel value
                current.setFlatPixel(pos,rgb)
    
    
    def jail(self):
        """
        Puts jail bars on the current image
        
        The jail should be built as follows:
        * Put 3-pixel-wide horizontal bars across top and bottom,
        * Put 4-pixel vertical bars down left and right, and
        * Put n 4-pixel vertical bars inside, where n is (number of columns - 8) // 50.
        
        The n+2 vertical bars should be as evenly spaced as possible.
        """
        current=self.getCurrent()
        self._drawVBar(0, (255,0,0))
        self._drawHBar(0, (255,0,0))
        self._drawVBar(current.getWidth()-4, (255,0,0))
        self._drawHBar(current.getHeight()-3, (255,0,0))
        n=(current.getWidth()-8)//50
        x=(current.getWidth()-8-4*n)/n
        for y in range(n):
            h=round((4*(y+1)+(y+1)*x))
            self._drawVBar(h, (255,0,0))
        
    
    def vignette(self):
        """
        Modifies the current image to simulates vignetting (corner darkening).
        
        Vignetting is a characteristic of antique lenses. This plus sepia tone helps
        give a photo an antique feel.
        
        To vignette, darken each pixel in the image by the factor
        
            1 - (d / hfD)^2
        
        where d is the distance from the pixel to the center of the image and hfD 
        (for half diagonal) is the distance from the center of the image to any of 
        the corners.
        """
        import math 
        current = self.getCurrent()
        for x in range(current.getHeight()):
            for y in range(current.getWidth()):
                hfD=math.sqrt((current.getWidth()/2)**2+(\
current.getHeight()/2)**2)
                d=math.sqrt((current.getHeight()/2-x)**2+(\
current.getWidth()/2-y)**2)
                rgb = current.getPixel(x,y)
                red   = (1 - (d / hfD)**2)*rgb[0]
                green = (1 - (d / hfD)**2)*rgb[1]
                blue  = (1 - (d / hfD)**2)*rgb[2]
                rgb = (int(red),int(green),int(blue)) # New pixel value
                current.setPixel(x,y,rgb)
    
    
    def pixellate(self,step):
        """
        Pixellates the current image to give it a blocky feel.
        
        To pixellate an image, start with the top left corner (e.g. the first row and
        column).  Average the colors of the step x step block to the right and down
        from this corner (if there are less than step rows or step columns, go to the
        edge of the image). Then assign that average to ALL of the pixels in that block.
        
        When you are done, skip over step rows and step columns to go to the next 
        corner pixel.  Repeat this process again.  The result will be a pixellated image.
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0
        """
        current = self.getCurrent()
        for y in range(0,current.getWidth(),step):
            for x in range(0,current.getHeight(),step):
                self.pixelavg(x,y,step)
                
                
    def pixelavg(self, x, y,step):
        """
        Procedure: Assigns average of the colors of the pixels within a block to each pixel in the block.
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int 3> 0
        
        Parameter x: The pixel row
        Precondition: x is an int >= 0 and < height
        
        Parameter y: The pixel column
        Precondition: y is an int >= 0 and < width
        """
        current = self.getCurrent()
        r=0
        g=0
        b=0

        for s in range(step):
            for h in range(step):
                if x+s<current.getHeight() and y+h<current.getWidth():
                    a=current.getPixel(x+s,y+h)
                    r+=a[0]
                    g+=a[1]
                    b+=a[2]
        avgr=r/step**2
        avgg=g/step**2
        avgb=b/step**2
        avgpixel=(round(avgr),round(avgg),round(avgb))
        for s in range(step):
            for h in range(step):
                if x+s<current.getHeight() and y+h<current.getWidth():
                    current.setPixel(x+s,y+h,avgpixel)
                
                
    def encode(self, text):
        """
        Returns: True if it could hide the given text in the current image; False otherwise.
        
        This method attemps to hide the given message text in the current image.  It uses
        the ASCII representation of the text's characters.  If successful, it returns
        True.
        
        If the text has more than 999999 characters or the picture does not have enough
        pixels to store the text, this method returns False without storing the message.
        
        A beginning marker has been added of 2 pixels length which is '}~' to
        recognize that the image actually contains a message.
        
        An ending marker has been added of 2 pixels length which is '~}' to
        recognize where the message ends.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        current=self.getCurrent()
        length=current.getLength()

        if len(text)>999999 or len(text)+4>length:
            return False
        else:
            mark1=chr(125)+chr(126)
            self._encode_pixel(mark1[0],0)
            self._encode_pixel(mark1[1],1)
            for x in range(len(text)):
                self._encode_pixel(text[x],x+2)
            mark2=chr(126)+chr(125)
            self._encode_pixel(mark2[0],len(text)+2)
            self._encode_pixel(mark2[1],len(text)+3)
            return True
            
        

    
    def decode(self):
        """
        Returns: The secret message stored in the current image. 
        
        If no message is detected, it returns None
        """
        current=self.getCurrent()
        length=current.getLength()
        
        i=''
        p=self._decode_pixel(0)
        if p==125:
            for y in range(2,length):
                if self._decode_pixel(y)==126:
                    return i
                i+=chr(self._decode_pixel(y))
                
            

                        
        return None
            
        
    
    
    # HELPER FUNCTIONS
    def _drawVBar(self, col, pixel):
        """
        Draws a vertical bar on the current image at the given coloumn.
        
        This method draws a vertical 4-pixel-wide bar at the given coloumn of the current
        image. This means that the bar includes the pixels coloumn, coloumn+1, coloumn+2 and coloumn+3.
        The bar uses the color given by the pixel value.
        
        Parameter col: The start of the coloumn to draw the bar
        Precondition: col is an int, with 0 <= col  &&  col+3 < image width
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        current = self.getCurrent()
        for row in range(current.getHeight()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row, col+1, pixel)
            current.setPixel(row, col+2, pixel)
            current.setPixel(row, col+3, pixel)
        
        
    def _drawHBar(self, row, pixel):
        """
        Draws a horizontal bar on the current image at the given row.
        
        This method draws a horizontal 3-pixel-wide bar at the given row of the current
        image. This means that the bar includes the pixels row, row+1, and row+2.
        The bar uses the color given by the pixel value.
        
        Parameter row: The start of the row to draw the bar
        Precondition: row is an int, with 0 <= row  &&  row+2 < image height
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        current = self.getCurrent()
        for col in range(current.getWidth()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row+1, col, pixel)
            current.setPixel(row+2, col, pixel)
    
    
    def _decode_pixel(self, pos):
        """
        Returns: the number n that is hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as the
        last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        rgb = self.getCurrent().getFlatPixel(pos)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10
    
    
    def _encode_pixel(self,letter,pos):
        """
        Procedure:encodes a letter into the pixel pos of the current image.
        
        This function assumes that the letter's ASCII value is a 3-digit number
        
        For the pixel overflow problem the issue will be solved as follows:
        if the r,g or b value exceeds 255 through encoding then the new value-10
        will be used to reassign the pixel value as the message encoded will still
        be retained
        
        Parameter letter: the letter to encode
        Precondition: letter is a string of length 1
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        a=ord(letter)
        b=str(a)
        if len(b)==2:
            b='0'+b
        elif len(b)==1:
            b='00'+b
        rgb = self.getCurrent().getFlatPixel(pos)
        v1=str(rgb[0])
        v2=str(rgb[1])
        v3=str(rgb[2])
        n1=v1[0:2]+b[0]
        n2=v2[0:2]+b[1]
        n3=v3[0:2]+b[2]
        if int(n1)>255:
            n1=str(int(n1)-10)
        if int(n2)>255:
            n2=str(int(n2)-10)
        if int(n3)>255:
            n3=str(int(n3)-10)
        pixel=(int(n1),int(n2),int(n3))
        
        self.getCurrent().setFlatPixel(pos,pixel)
    