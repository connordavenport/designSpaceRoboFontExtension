import vanilla
from mojo.UI import MultiLineView, splitText
from mojo.subscriber import WindowController, Subscriber, registerRoboFontSubscriber

from mojo.roboFont import RFont, RGlyph


#import importlib
#import ufoProcessor
#importlib.reload(ufoProcessor)

class InstancesPreview(Subscriber, WindowController):

    debug = True

    def build(self, operator=None):
        self.operator = operator
        dummyFont = RFont(showInterface=False)

        self.w = vanilla.FloatingWindow((700, 400), "Instances Preview", minSize=(500, 300))
        self.w.input = vanilla.EditText((10, 10, -120, 22), callback=self.inputCallback)
        self.w.singleLine = vanilla.CheckBox((-100, 10, 100, 22), "Single line", value=True, callback=self.singleLineCheckboxCallback)
        self.w.hl = vanilla.HorizontalLine((0, 41, 0, 1))
        self.w.preview = MultiLineView((0, 42, 0, 0), pointSize=40, displayOptions=dict(Beam=False))
        self.w.preview.setFont(dummyFont)

    def started(self):
        self.w.open()

    def inputCallback(self, sender):
        glyphNames = splitText(sender.get(), self.operator.getCharacterMapping())
        #print("glyphNames", glyphNames)
        glyphs = []
        for instance in self.operator.instances:
            #print('instancesPreviewer', instance.location)
            for glyphName in glyphNames:
                # do not bend, reasoning: the instance locations are in designspace values.
                glyph = self.operator.makeOneGlyph(glyphName, instance.location, decomposeComponents=True)
                if glyph is not None:
                    dest = RGlyph()
                    dest.fromMathGlyph(glyph)
                    dest.name = glyph.name
                    glyphs.append(dest)
            if self.w.singleLine.get():
                glyphs.append(self.w.preview.createNewLineGlyph())
        self.w.preview.set(glyphs)

    designspaceEditorInstancesDidChangeDelay = 0.1

    def singleLineCheckboxCallback(self, sender):
        self.inputCallback(self.w.input)

    def designspaceEditorInstancesDidChange(self, notification):
        self.inputCallback(self.w.input)

    #def designspaceEditorInstancesDidChangeSelection(self, notification):
    #    print("designspaceEditorInstancesDidChangeSelection")
    #    print(notification)

    def designspaceEditorSourcesDidChanged(self, notification):
        self.inputCallback(self.w.input)

    def designspaceEditorAxesDidChange(self, notification):
        self.inputCallback(self.w.input)



if __name__ == '__main__':
    c = InstancesPreview(operator=CurrentDesignspace())
    c.w.input.set("HELLO")
    c.inputCallback(c.w.input)