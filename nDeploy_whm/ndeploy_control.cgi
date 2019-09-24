#!/usr/bin/python

import cgi
import cgitb
import os
import yaml
import psutil
import platform
from commoninclude import return_label, return_prepend, bcrumb, print_header, print_footer, print_modals, print_loader, cardheader, cardfooter

__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Production"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ndeploy_control_file = installation_path+"/conf/ndeploy_control.yaml"
branding_file = installation_path+"/conf/branding.yaml"
autom8n_version_info_file = installation_path+"/conf/version.yaml"

cgitb.enable()

form = cgi.FieldStorage()

# nDeploy Control
if os.path.isfile(ndeploy_control_file):
    with open(ndeploy_control_file, 'r') as ndeploy_control_data_file:
        yaml_parsed_ndeploy_control_settings = yaml.safe_load(ndeploy_control_data_file)
    ndeploy_theme_color = yaml_parsed_ndeploy_control_settings.get("ndeploy_theme_color", "light")
    primary_color = yaml_parsed_ndeploy_control_settings.get("primary_color", "#121212")
    logo_url = yaml_parsed_ndeploy_control_settings.get("logo_url", "None")
    app_email = yaml_parsed_ndeploy_control_settings.get("app_email", "None")
else:
    ndeploy_theme_color = "light"
    primary_color = "#121212"
    logo_url = "None"
    app_email = "None"

# Branding Support
if os.path.isfile(branding_file):
    with open(branding_file, 'r') as brand_data_file:
        yaml_parsed_brand = yaml.safe_load(brand_data_file)
    brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    brand = yaml_parsed_brand.get("brand", "AUTOM8N")
    brand_group = yaml_parsed_brand.get("brand_group", "NGINX AUTOMATION")
    brand_anchor = yaml_parsed_brand.get("brand_anchor", "A U T O M 8 N")
    brand_link = yaml_parsed_brand.get("brand_link", "https://autom8n.com/")
else:
    brand_logo = "xtendweb.png"
    brand = "AUTOM8N"
    brand_group = "NGINX AUTOMATION"
    brand_anchor = "A U T O M 8 N"
    brand_link = "https://autom8n.com/"

print_header(brand+' Control Center')
bcrumb(brand+' Control Center','fas fa-tools')

# Plugin Status
nginx_status = False
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
    else:
        mycmdline = myprocess.cmdline()
    if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
        nginx_status = True

watcher_status="status"

# Get version of Nginx and plugin
with open(autom8n_version_info_file, 'r') as autom8n_version_info_yaml:
    autom8n_version_info_yaml_parsed = yaml.safe_load(autom8n_version_info_yaml)
autom8n_version = autom8n_version_info_yaml_parsed.get('autom8n_version')

print('     <!-- Dash Widgets Start -->')
print('     <div id="dashboard" class="row">')

# Nginx Status
print('         <div class="col-sm-6 col-xl-3"> <!-- Dash Row Start -->')

cardheader('')
print('             <div class="card-body text-center"> <!-- Card Body Start -->')
print('                 <h4 class="mb-0">Plugin Status</h4>')
print('                 <ul class="list-unstyled mb-0">')
print('                     <li><small>'+brand+' '+autom8n_version.replace("Autom8n ",'')+'</small></li>')

if nginx_status:
    print('                 <li class="mt-2 text-success">Enabled <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                 <li class="mt-2 text-danger">Disabled <i class="fas fa-power-off ml-1"></i></li>')

print('                 </ul>')
print('             </div>')

if nginx_status:
    print('         <form id="disable_ndeploy" class="form" onsubmit="return false;">')
    print('             <button class="btn btn-secondary btn-block mb-0">Disable</button>')
    print('             <input hidden name="plugin_status" value="disable">')
else:
    print('         <form id="enable_ndeploy" class="form" onsubmit="return false;">')
    print('             <button class="btn btn-secondary btn-block mb-0">Enable</button>')
    print('             <input hidden name="plugin_status" value="enable">')

print('             </form>')
print('         </div> <!-- Dash Row End -->')
cardfooter('')

print('     </div> <!-- Dash Widgets End -->')

print('     <!-- WHM Starter Row -->')
print('     <div class="row justify-content-lg-center flex-nowrap">')

print('')
print('         <!-- Secondary Navigation -->')
print('         <div class="pl-3 col-md-3 nav flex-column nav-pills d-none d-lg-block d-xl-block d-xs-none d-sm-none" id="v-pills-tab" role="tablist" aria-orientation="vertical">')
print('             <a class="nav-link active" id="v-pills-home-tab" data-toggle="pill" href="#v-pills-home" role="tab" aria-controls="v-pills-home">Home</a>')
print('             <a class="nav-link" id="v-pills-branding-tab" data-toggle="pill" href="#v-pills-branding" role="tab" aria-controls="v-pills-branding">Branding</a>')
print('             <a class="nav-link" id="v-pills-aesthetics-tab" data-toggle="pill" href="#v-pills-aesthetics" role="tab" aria-controls="v-pills-aesthetics">Aesthetics</a>')
print('             <a class="nav-link" id="v-pills-php_backends-tab" data-toggle="pill" href="#v-pills-php_backends" role="tab" aria-controls="v-pills-php_backends">PHP&nbsp;Backends</a>')
print('             <a class="nav-link" id="v-pills-netdata-tab" data-toggle="pill" href="#v-pills-netdata" role="tab" aria-controls="v-pills-netdata">Netdata</a>')
print('             <a class="nav-link" id="v-pills-glances-tab" data-toggle="pill" href="#v-pills-glances" role="tab" aria-controls="v-pills-glances">Glances</a>')
print('             <a class="nav-link" id="v-pills-modules-tab" data-toggle="pill" href="#v-pills-modules" role="tab" aria-controls="v-pills-modules">Modules</a>')
print('         </div>')
print('')
print('         <div class="tab-content col-md-12 col-lg-9" id="v-pills-tabContent">')

print('             <!-- Secondary Mobile Navigation -->')
print('             <div class="d-lg-none d-xl-none dropdown nav">')
print('                 <button class="btn btn-primary btn-block dropdown-toggle mb-3" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">')
print('                     Config Menu')
print('                 </button>')
print('                 <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">')
print('                     <a class="dropdown-item" id="v-pills-home-tab" data-toggle="pill" href="#v-pills-home" role="tab" aria-controls="v-pills-home" aria-pressed="false">Home</a>')
print('                     <a class="dropdown-item" id="v-pills-branding-tab" data-toggle="pill" href="#v-pills-branding" role="tab" aria-controls="v-pills-branding" aria-pressed="false">Branding</a>')
print('                     <a class="dropdown-item" id="v-pills-aesthetics-tab" data-toggle="pill" href="#v-pills-aesthetics" role="tab" aria-controls="v-pills-aesthetics" aria-pressed="false">Aesthetics</a>')
print('                     <a class="dropdown-item" id="v-pills-php_backends-tab" data-toggle="pill" href="#v-pills-php_backends" role="tab" aria-controls="v-pills-php_backends" aria-pressed="false">PHP&nbsp;Backends</a>')
print('                     <a class="dropdown-item" id="v-pills-netdata-tab" data-toggle="pill" href="#v-pills-netdata" role="tab" aria-controls="v-pills-netdata" aria-pressed="false">Netdata</a>')
print('                     <a class="dropdown-item" id="v-pills-glances-tab" data-toggle="pill" href="#v-pills-glances" role="tab" aria-controls="v-pills-glances" aria-pressed="false">Glances</a>')
print('                     <a class="dropdown-item" id="v-pills-modules-tab" data-toggle="pill" href="#v-pills-modules" role="tab" aria-controls="v-pills-modules" aria-pressed="false">Modules</a>')
print('                 </div>')
print('             </div>')

# Home Tab
print('')
print('             <!-- Home Tab -->')
print('             <div class="tab-pane fade show active" id="v-pills-home" role="tabpanel" aria-labelledby="v-pills-home-tab">')

cardheader('Welcome to '+brand+' Control','fas fa-tools')

print('                 <div class="card-body p-0"> <!-- Card Body Start -->')
print('                     <div class="row no-gutters row-1"> <!-- Row Start -->')
print('                         <div class="col-md-6 alert"><i class="fas fa-infinity"></i> '+brand+' cPanel Plugin</div>')
print('                             <div class="col-md-6">')
print('                                 <div class="row no-gutters">')

nginx_status = False
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
    else:
        mycmdline = myprocess.cmdline()
    if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
        nginx_status = True

if nginx_status:
    print('                                 <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
    print('                                 <div class="col-9">')
    print('                                     <form id="disable_ndeploy" class="form" onsubmit="return false;">')
    print('                                         <button type="submit" class="alert btn btn-info">Disable</button>')
    print('                                         <input hidden name="plugin_status" value="disable">')
else:
    print('                                 <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
    print('                                 <div class="col-9">')
    print('                                     <form id="enable_ndeploy" class="form" onsubmit="return false;">')
    print('                                     <button type="submit" class="alert btn btn-info">Enable</button>')
    print('                                     <input hidden name="plugin_status" value="enable">')

print('                                     </form>')
print('                                 </div>')
print('                             </div>')
print('                         </div>')
print('                     </div> <!-- Row End -->')
print('                 </div> <!-- Card Body End -->')
print('                 <div class="card-body"> <!-- Card Body Start -->')
print('                     <p class="small mb-0">Welcome to the '+brand+' Control Center. Here you will have control over various theming, branding, and configuration settings for this application. You can enable and disable the application above.</p>')
print('                 </div> <!-- Card Body End -->')
cardfooter('')

print('             </div> <!-- End Home Tab -->')

# Branding Tab
print('')
print('                <!-- Branding Tab -->')
print('                <div class="tab-pane fade" id="v-pills-branding" role="tabpanel" aria-labelledby="v-pills-branding-tab">')

cardheader('Branding Settings','fas fa-infinity')
brand_hint = " Enter the textual name you want to represent this application as for whitelabeling purposes. This shows up in both WHM, cPanel, and this application. "
brand_logo_hint = " Enter the filename of the brand icon used for this application. This file must exist in the suggested directories or rebuild will fail. "
brand_group_hint = " cPanel creates sections for content. Enter the section title you want this application to show up in. "
brand_anchor_hint = " The textual part of the link that is located in the footer of this application. "
brand_link_hint = " This is the link that is attached to the above 'Footer Anchor Text' for use on the footer of the application. "

print('                        <div class="card-body"> <!-- Card Body Start -->')
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->')
print('                                <form class="form w-100" id="ndeploy_control_branding" method="post" onsubmit="return false;">')

print('                                    <label class="small" for="brand">Personalize the application name for cPanel\'s and WHM\'s icon label, as well as the header of this application. <em>The brand name must contain only letters, numbers, hyphens, or underscores otherwise the brand rebuild will fail.</em></label>')
print('                                    <div class="input-group mb-4">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_desc">')
print('                                                '+return_prepend("Brand Name", brand_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" name="brand" value="'+brand+'" id="brand" aria-describedby="brand_desc">')
print('                                    </div>')

print('                                    <label class="small" for="brand_logo">Enter the filename of the 48x48 pixel brand icon that has been uploaded to the <kbd>'+installation_path+'/nDeploy_whm</kbd> and <kbd>'+installation_path+'/nDeploy_cp</kbd> folders to properly brand cPanel, WHM, and this application.</label>')
print('                                    <div class="input-group mb-4">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_logo_desc">')
print('                                                '+return_prepend("Brand Icon", brand_logo_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" name="brand_logo" value="'+brand_logo+'" id="brand_logo" aria-describedby="brand_logo_desc">')
print('                                    </div>')


print('                                    <label class="small" for="brand_group">Enter the section you want this application to be placed in within each user\'s cPanel.</label>')
print('                                    <div class="input-group mb-4">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_group_desc">')
print('                                                '+return_prepend("cPanel Section", brand_group_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" name="brand_group" value="'+brand_group+'" id="brand_group" aria-describedby="brand_group_desc">')
print('                                    </div>')

print('                                    <label class="small" for="brand_anchor">Enter your brand\'s anchor text that will be used on the footer of the application.</label>')
print('                                    <div class="input-group mb-4">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_anchor_desc">')
print('                                                '+return_prepend("Footer Anchor Text", brand_anchor_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" name="brand_anchor" value="'+brand_anchor+'" id="brand_anchor" aria-describedby="brand_anchor_desc">')
print('                                    </div>')

print('                                    <label class="small" for="brand_link">Enter your brand\'s website link that the above anchor text will link to via the footer.</label>')
print('                                    <div class="input-group mb-4">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_link_desc">')
print('                                                '+return_prepend("Footer Link", brand_link_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" name="brand_link" value="'+brand_link+'" id="brand_link" aria-describedby="brand_link_desc">')
print('                                    </div>')
print('                                    <button class="mb-3 btn btn-outline-primary btn-block" type="submit">Save Branding Options</button>')
print('                                </form>')

print('                                <form class="form w-100" id="restore_branding_defaults" method="post" onsubmit="return false;">')
print('                                    <input hidden class="form-control" name="restore_defaults" value="enabled">')
print('                                    <button class="btn btn-outline-primary btn-block" type="submit">Restore Branding Defaults</button>')
print('                                </form>')
print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->')

cardfooter('')

print('                </div> <!-- End Branding Tab -->')

# Aesthetics Tab
print('')
print('                <!-- Aesthetics Tab -->')
print('                <div class="tab-pane fade" id="v-pills-aesthetics" role="tabpanel" aria-labelledby="v-pills-aesthetics-tab">')

cardheader(brand+' Aesthetics', 'fas fa-palette')
primary_color_hint = " This can be a HEX code, a RGB color code, or a HTML color name like ghostwhite, grey, black, etc. "
ndeploy_theme_color_hint = " Choose between a light or dark theme. "
logo_url_hint = " This is the logo URL used in the header. "
app_email_hint = " Enter the email address this application will use when users hit a bind. This email will show up at useful times. "

print('                        <div class="card-body"> <!-- Card Body Start -->')
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->')
print('                                <form class="form w-100" id="ndeploy_control_config" method="post" onsubmit="return false;">')

print('                                <label class="small" for="primary_color">Enter the primary color used throughout the application. Use this to accent branding colors.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="primary_color_desc">')
print('                                            '+return_prepend("Primary Application Color", primary_color_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="primary_color" value="'+primary_color+'" id="primary_color" aria-describedby="primary_color_desc">')
print('                                </div>')

print('                                <label class="small" for="ndeploy_theme_color">Select a theme to use with the application.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <label class="input-group-text">'+return_prepend("Theme", ndeploy_theme_color_hint)+'</label>')
print('                                    </div>')
print('                                    <select name="ndeploy_theme_color" class="custom-select">')

bootstrap_colors = ['light', 'dark']
for color in bootstrap_colors:
    if ndeploy_theme_color != color:
        print('                                        <option value="'+color+'">'+color+'</option>')
    else:
        print('                                        <option selected value="'+color+'">'+color+'</option>')
print('                                    </select>')
print('                                </div>')

print('                                <label class="small" for="logo_url">Enter the logo URL to use in the header instead of the default icon and brand name. Set this to <kbd>None</kbd> to disable.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="logo_url_desc">')
print('                                            '+return_prepend("Logo URL", logo_url_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="logo_url" value="'+logo_url+'" id="logo_url" aria-describedby="logo_url_desc">')
print('                                </div>')

print('                                <label class="small" for="app_email">Enter a support email for users if they run into various issues. Set this to <kbd>None</kbd> to disable.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="app_email_desc">')
print('                                            '+return_prepend("Support E-mail", app_email_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="app_email" value="'+app_email+'" id="app_email" aria-describedby="app_email_desc">')
print('                                </div>')

print('                                <button class="mb-3 btn btn-outline-primary btn-block" type="submit">Save Aesthetics Settings</button>')
print('                                </form>')

print('                                <form class="form w-100" id="restore_ndeploy_control_defaults" method="post" onsubmit="return false;">')
print('                                    <input hidden class="form-control" name="restore_defaults" value="enabled">')
print('                                    <button class="btn btn-outline-primary btn-block" type="submit">Restore Aesthetics Defaults</button>')
print('                                </form>')


print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->')

cardfooter('')

print('                </div> <!-- End Aesthetics Tab -->')

# PHP Installer
print('')
print('                <!-- PHP Backends Tab -->')
print('                <div class="tab-pane fade" id="v-pills-php_backends" role="tabpanel" aria-labelledby="v-pills-php_backends-tab">')

cardheader('Setup PHP Backends', 'fab fa-php')

print('                        <div class="card-body"> <!-- Card Body Start -->')
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->')
print('                                <p class="small">Welcome to the Easy PHP Installer. This will configure NGINX to use the cPanel PHP packages (EA-PHPxx-) as direct upstreams. These versions will be selectable under the \'PHP\' category when choosing an upstream. <em>This process can take between 1 to 3 minutes depending on processing power and connection speed.</em></p>')
print('                                <form class="form w-100" id="easy_php_setup" method="post" onsubmit="return false;">')
print('                                    <input hidden class="form-control" name="run_installer" value="enabled">')
print('                                    <button class="btn btn-outline-primary btn-block" type="submit">Install Native nGinx PHP Support</button>')
print('                                </form>')
print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->')

cardfooter('')

print('                </div> <!-- End PHP Backends Tab -->')

# Netdata Tab
print('')
print('                <!-- Netdata Tab -->')
print('                <div class="tab-pane fade" id="v-pills-netdata" role="tabpanel" aria-labelledby="v-pills-netdata-tab">')

cardheader('Netdata Setup', 'fab fa-centos')
netdata_pass = ""
netdata_pass_hint = " Enter the password to access Netdata. "
print('                        <div class="card-body"> <!-- Card Body Start -->')
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->')
print('                                <form class="form w-100" id="easy_netdata_setup" method="post" onsubmit="return false;">')
print('                                    <p class="small">Welcome to the Netdata Installer. Netdata is distributed, real-time, performance and health monitoring for systems and applications. Netdata provides unparalleled insights, in real-time, of everything happening on the systems it runs (including web servers, databases, applications), using highly interactive web dashboards. <em>The Netdata installation process can take up to a minute depending on processing power and connection speed.</em></p>')
if not os.path.isfile('/etc/nginx/conf.d/netdata.password'):
    print('                                    <label class="small" for="netdata_pass">The Netdata username is <kbd>netdata</kbd>. Enter the password you wish to use to access the Netdata Monitoring System.</label>')
    print('                                    <div class="input-group mb-4">')
    print('                                        <div class="input-group-prepend">')
    print('                                            <span class="input-group-text" id="netdata_pass_desc">')
    print('                                                '+return_prepend("Netdata Password", netdata_pass_hint))
    print('                                            </span>')
    print('                                        </div>')
    print('                                        <input type="text" class="form-control" name="netdata_pass" value="'+netdata_pass+'" id="netdata_pass" aria-describedby="netdata_pass_desc">')
    print('                                    </div>')
print('                                    <input hidden class="form-control" name="run_installer" value="enabled">')
print('                                    <input hidden class="form-control" name="netdata_pass" value="'+netdata_pass+'">')
if os.path.isfile('/etc/nginx/conf.d/netdata.password'):
    print('                                    <button class="mb-3 btn btn-outline-primary btn-block" type="submit">Reinstall Netdata Monitoring System</button>')
else:
    print('                                    <button class="mb-3 btn btn-outline-primary btn-block" type="submit">Install Netdata Monitoring System</button>')
print('                                </form>')

if os.path.isfile('/etc/nginx/conf.d/netdata.password'):
    print('                                <form class="form w-100" id="clear_netdata_credentials" method="post" onsubmit="return false;">')
    print('                                    <input hidden class="form-control" name="remove_netdata_creds" value="enabled">')
    print('                                    <button class="btn btn-outline-primary btn-block" type="submit">Remove Netdata Credentials</button>')
    print('                                </form>')

print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->')

cardfooter('')

print('                </div> <!-- End Netdata Tab -->')

# Glances Tab
print('')
print('                <!-- Glances Tab -->')
print('                <div class="tab-pane fade" id="v-pills-glances" role="tabpanel" aria-labelledby="v-pills-glances-tab">')

cardheader('Glances Setup', 'fab fa-centos')
glances_pass = ""
glances_pass_hint = " Enter the password to access Glances. "
print('                        <div class="card-body"> <!-- Card Body Start -->')
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->')
print('                                <form class="form w-100" id="easy_glances_setup" method="post" onsubmit="return false;">')
print('                                    <p class="small">Welcome to the Glances Installer. Glances is a cross-platform system monitoring tool written in Python. <em>The Glances installation process can take up to a minute depending on processing power and connection speed.</em></p>')
if not os.path.isfile('/etc/nginx/conf.d/glances.password'):
    print('                                    <label class="small" for="glances_pass">The Glances username is <kbd>glances</kbd>. Enter the password you wish to use to access the Glances Monitoring System.</label>')
    print('                                    <div class="input-group mb-4">')
    print('                                        <div class="input-group-prepend">')
    print('                                            <span class="input-group-text" id="glances_pass_desc">')
    print('                                                '+return_prepend("Glances Password", glances_pass_hint))
    print('                                            </span>')
    print('                                        </div>')
    print('                                        <input type="text" class="form-control" name="glances_pass" value="'+glances_pass+'" id="glances_pass" aria-describedby="glances_pass_desc">')
    print('                                    </div>')
print('                                    <input hidden class="form-control" name="run_installer" value="enabled">')
print('                                    <input hidden class="form-control" name="glances_pass" value="'+glances_pass+'">')
if os.path.isfile('/etc/nginx/conf.d/glances.password'):
    print('                                    <button class="mb-3 btn btn-outline-primary btn-block" type="submit">Reinstall Glances Monitoring System</button>')
else:
    print('                                    <button class="mb-3 btn btn-outline-primary btn-block" type="submit">Install Glances Monitoring System</button>')
print('                                </form>')

if os.path.isfile('/etc/nginx/conf.d/glances.password'):
    print('                                <form class="form w-100" id="clear_glances_credentials" method="post" onsubmit="return false;">')
    print('                                    <input hidden class="form-control" name="remove_glances_creds" value="enabled">')
    print('                                    <button class="btn btn-outline-primary btn-block" type="submit">Remove Glances Credentials</button>')
    print('                                </form>')

print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->')

cardfooter('')

print('                </div> <!-- End Glances Tab -->')

# Modules Tab
print('')
print('                <!-- Modules Tab -->')
print('                <div class="tab-pane fade" id="v-pills-modules" role="tabpanel" aria-labelledby="v-pills-modules-tab">')
print('                <form id="module-installer" class="form" onsubmit="return false;">')

cardheader(brand+' Modules Setup', 'fab fa-centos')
test_cookie_hint = " Controls loading of nginx-nDeploy-module-testcookie_access which allows good bots in while keeping bad bots out. "
mod_security_hint = " Controls loading of nginx-nDeploy-module-modsecurity which installs the Mod Security v3 Web Application Firewall. "
pagespeed_hint = " Controls loading of nginx-nDeploy-module-pagespeed which delivers PageSpeed-optimized pages. "
brotli_hint = " Controls loading of nginx-nDeploy-module-brotli which is a newer bandwidth optimization created by Google. "
geoip2_hint = " Controls loading of nginx-nDeploy-module-geoip2 which creates variables based on the client IP address. "

print('                        <div class="card-body"> <!-- Card Body Start -->')
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->')

print('                                '+return_label("Bot Mitigate Module", test_cookie_hint))
print('                                <div class="col-md-6 pr-0">')
print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
if os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="test_cookie" value="enabled" autocomplete="off" checked> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="test_cookie" value="disabled" autocomplete="off"> Uninstalled')
    print('                                        </label>')
else:
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="test_cookie" value="enabled" autocomplete="off"> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="test_cookie" value="disabled" autocomplete="off" checked> Uninstalled')
    print('                                        </label>')
print('                                    </div>')
print('                                </div>')

print('                                '+return_label("ModSecurity V3 Module", mod_security_hint))
print('                                <div class="col-md-6 pr-0">')
print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
if os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="mod_security" value="enabled" autocomplete="off" checked> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="mod_security" value="disabled" autocomplete="off"> Uninstalled')
    print('                                        </label>')
else:
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="mod_security" value="enabled" autocomplete="off"> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="mod_security" value="disabled" autocomplete="off" checked> Uninstalled')
    print('                                        </label>')
print('                                    </div>')
print('                                </div>')

print('                                '+return_label("PageSpeed Module", pagespeed_hint))
print('                                <div class="col-md-6 pr-0">')
print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
if os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="pagespeed" value="enabled" autocomplete="off" checked> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="pagespeed" value="disabled" autocomplete="off"> Uninstalled')
    print('                                        </label>')
else:
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="pagespeed" value="enabled" autocomplete="off"> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="pagespeed" value="disabled" autocomplete="off" checked> Uninstalled')
    print('                                        </label>')
print('                                    </div>')
print('                                </div>')

print('                                '+return_label("Brotli Module", brotli_hint))
print('                                <div class="col-md-6 pr-0">')
print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
if os.path.isfile('/etc/nginx/modules.d/brotli.load'):
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="brotli" value="enabled" autocomplete="off" checked> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="brotli" value="disabled" autocomplete="off"> Uninstalled')
    print('                                        </label>')
else:
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="brotli" value="enabled" autocomplete="off"> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="brotli" value="disabled" autocomplete="off" checked> Uninstalled')
    print('                                        </label>')
print('                                    </div>')
print('                                </div>')

print('                                '+return_label("Geoip2 Module", geoip2_hint))
print('                                <div class="col-md-6 pr-0">')
print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
if os.path.isfile('/etc/nginx/modules.d/geoip2.load'):
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="geoip2" value="enabled" autocomplete="off" checked> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="geoip2" value="disabled" autocomplete="off"> Uninstalled')
    print('                                        </label>')
else:
    print('                                        <label class="btn btn-light">')
    print('                                            <input type="radio" name="geoip2" value="enabled" autocomplete="off"> Installed')
    print('                                        </label>')
    print('                                        <label class="btn btn-light active">')
    print('                                            <input type="radio" name="geoip2" value="disabled" autocomplete="off" checked> Uninstalled')
    print('                                        </label>')


print('                                    </div>')
print('                                </div>')
print('                                <button class="mt-2 btn btn-outline-primary btn-block" type="submit">Apply Module Selection</button>')
print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->')

cardfooter('Note that each module increases NGINX size and processing requirements, so only install the required functionality for best performance.')

print('                </form>')
print('                </div> <!-- End Modules Tab -->')

print('                <!-- Column End -->')
print('                </div>')
print('')
print('            <!-- WHM End Row -->')
print('            </div>')

print_footer()

print('        </div> <!-- Main Container End -->')
print('')

print_modals()
print_loader()

print('    <!-- Body End -->')
print('    </body>')
print('</html>')