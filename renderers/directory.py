import os
import math
from base import BaseRenderer

#CONSTANTS
STEP = 20  # links per row
RADIUS = 12

#tau makes trig math so much easier
tau = 2*math.pi

#utility functions
def is_hidden(path):
    #linux only for now
    return os.path.basename(path).startswith(".")

class DirectoryRenderer(BaseRenderer):

    def render(self, path):
        return self.render_dir(path)

    def can_render(self, path):
        return os.path.isdir(path)

    def render_dir(self, path):
        """
        Returns the JanusVR HTML for rendering a dir
        """
        #filter out hidden paths to avoid clutter
        dirs = [ x for x in os.listdir(path) if not is_hidden(path+'/'+x)]
        dirs.sort()

        html = """
        <html>
        <head>
        <title>Browser</title>
        </head>
        <body>
        <FireBoxRoom>
        <Assets>
        <AssetImage id="folder_png_janus_ui" src="/~~/images/folder.png" />
        <AssetImage id="file_png_janus_ui" src="/~~/images/file.png" />

        """

        for i, d in enumerate(dirs):
            if os.path.isfile(path+'/'+d):
                html += self.render_asset(path, d)

        html += """
        </Assets>
        <Room use_local_asset="room_plane" visible='false' gravity="-3.0" jump_velocity="10.0" walk_speed="8.0" run_speed="16.0" >
        """

        for i, d in enumerate(dirs):
            html += self.render_item(i, path, d)

        html += """
        </Room>
        </FireBoxRoom>
        </body>
        </html>
         """
        return html


    def render_asset(self, p, d):
        if d.lower().endswith((".jpg", '.jpeg', '.gif', '.png')):
            return """
            <AssetImage id="{name}" src="{src}" />
            """.format(name=d.replace('.', '_'), src=p+'/'+d)
        else:
            return ""

    def render_item(self, i, p, d):
        if os.path.isdir(p+'/'+d):
            return """
            <Link pos="{pos}"  url="{link}" {fwd} scale="2.0 3.0 1" col="0.6 1 0.6"  title="{title}" thumb_id="folder_png_janus_ui" />
            """.format(pos="%s %s %s" % self.get_pos(i), fwd=self.get_fwd(i), link=d+"/", title=d)

        elif d.lower().endswith((".jpg", '.jpeg', '.gif', '.png')):
            return """
            <Image id="{name}" pos="{pos}"  url="{link}" {fwd}   title="{title}" />
            """.format(name=os.path.split(d)[1].replace('.', '_'), pos="%s %s %s" % self.get_pos(i), fwd=self.get_fwd(i),
                       link=d+"/", title=d)
        else:
            return """<Link pos="{pos}"  url="{link}" {fwd} scale="2.0 3.0 1" col="0.6 0.6 1"  title="{title}" thumb_id="file_png_janus_ui" />
            """.format(pos="%s %s %s" % self.get_pos(i), fwd=self.get_fwd(i), link=d, title=d)

    def get_pos(self, i):
        theta = (i*tau/STEP) + tau/4
        x = RADIUS*math.cos(theta)
        y = 0
        z = RADIUS*math.sin(theta)

        while theta >= tau + tau/4:
            theta -= tau
            y += 4

        return (x, y, z)

    def get_fwd(self, i):

        # we want to to rotate our positional angle *plus* 90 degrees to make it perpendicular so we're facing the
        # center of the circle
        theta = (i*tau/STEP) + tau/2

        # rotation matrix around the y axis
        result_x = ' xdir="%s %s %s" ' % (math.cos(theta), 0, math.sin(theta))
        result_y = ' ydir="0 1 0" '
        result_z = ' zdir="%s %s %s" ' % (-1*math.sin(theta), 0, math.cos(theta))
        return result_x + result_y + result_z