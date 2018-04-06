import maya.cmds as cmds

#we need to use a class approach to make it easier for controls to call it own functions.
class MR_Texture_Relink_Window(object):

    def __init__(self):
        self.window = 'MR_Texture_Relink_Window';
        self.title = 'Texture Relink Tool';
        self.size = (546, 350);

    def create(self):

        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True);

        self.window = cmds.window(self.window, title=self.title, widthHeight = self.size);

        # add a form layout to window
        self.mainForm = cmds.formLayout(numberOfDivisions=100, );

        # add title
        self.titleDisplay = cmds.text(label = self.title, align="center", font="boldLabelFont" );
        # position title on the top left of the screen
        cmds.formLayout(self.mainForm, edit=True, attachForm=(  [self.titleDisplay, 'top', 5],
                                                                [self.titleDisplay, 'left', 5],
                                                                [self.titleDisplay, 'right', 5])
                        );

        #add sperator
        self.titleSeperator = cmds.separator();
        # position seperator
        cmds.formLayout(self.mainForm, edit=True, attachControl=[self.titleSeperator, 'top', 10, self.titleDisplay],
                                                  attachForm=([self.titleSeperator, 'left', 5],
                                                             [self.titleSeperator, 'right', 5])
                        );

        # add button
        self.btnFolderSet = cmds.button(label='Set Texture Folder', height=30, width=150, command=self.SetFolderBtnCmd);
        # position button
        cmds.formLayout(self.mainForm, edit=True, attachControl=[self.btnFolderSet, 'top', 20, self.titleDisplay],
                                                  attachForm=[self.btnFolderSet, 'left', 5]);

        #add folder location textfield
        self.txtFieldFolderLocation = cmds.textField(text="set location");
        #position textField
        cmds.formLayout(self.mainForm, edit=True, attachControl=([self.txtFieldFolderLocation, 'top', 24, self.titleDisplay],
                                                                 [self.txtFieldFolderLocation, 'left', 5, self.btnFolderSet]),
                                                  attachForm=[self.txtFieldFolderLocation, 'right', 5]);

        # add button
        self.btnRelinkTextures = cmds.button(label='Relink Textures', height=30, width=150, command=self.relinkBtnCmd);
        # position button
        cmds.formLayout(self.mainForm, edit=True, attachControl=[self.btnRelinkTextures, 'top', 5, self.btnFolderSet],
                                                  attachForm=[self.btnRelinkTextures, 'left', 5]);


        cmds.showWindow();

    # function called when set folder button is clicked
    def SetFolderBtnCmd(self, *args):
        cmds.fileBrowserDialog(mode=4, fc=self.relinkFolder, an='Set Folder', om='Reference')

    # function called when folder is set in set file broser dialogue
    def relinkFolder(self, fileName, fileType):
        cmds.textField(self.txtFieldFolderLocation, edit=True, text=fileName);

    # function called when the relink button is pressed.
    def relinkBtnCmd(self, *args):

        #get the path specified in the text field using a query
        basePath = cmds.textField(self.txtFieldFolderLocation, query=True, text=True);

        # list all file nodes
        fileNodes = cmds.ls(type="file")

        # repeat for each node
        for node in fileNodes:
            #get the current path
            currPath = cmds.getAttr(node + '.fileTextureName')

            #split the path name at the last folder
            pathSplit = currPath.split("/") #get positon of last '/'
            filename = pathSplit[-1] # split filename

            #combine basePath and filename to create a new path
            newPath = "%s/%s" %(basePath, filename)

            # set the path in the texture node
            cmds.setAttr(node + '.fileTextureName', newPath, type='string')

#run the programm
texRelinkWindow = MR_Texture_Relink_Window();
texRelinkWindow.create();