module.exports = function(grunt) {

    'use strict';

    grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
   
    jshint: {
        all: ['Gruntfile.js']
    },
 
    less: {
        development: {
            options: {
                paths: ["less/"],
                yuicompress: true
            },
        
            files: {
                "style.css": "less/style.less",
                "calendar.css": "less/calendar.less"
            }
        }
    },

    concat: {
        options: {
            separator: "",
        },
        style: {
            src: ["style.css",
                  "calendar.css",
                  "gallery.css",
                  'main.css',
                  'site.css',
                  'bootstrap.min.css',
                  'font-awesome.min.css',
                  'jquery.mobile-1.4.5.css',
                  '../js/jquery-ui-1.9.2.custom/css/ui-lightness/jquery-ui-1.9.2.custom.css',
                  'normalize.min.css'
                ],
        dest: 'site.css',
        }
    }, 

    cssmin: {
        options: {
            shorthandCompacting: false,
            roundingPrecision: -1,
            report: 'gzip'
        },
        minify: {
            files: {
              'site.min.css': ['site.css']
            }
        }
    },

    uglify: {
        dev: {
            options : {
                mangle: false,
                compress: false,
                beautify: true
            },
            src: ["../js/jquery-2.1.1.js",
                  "../js/jquery-ui-1.9.2.custom/js/jquery-ui-1.9.2.custom.js",
                  "../js/bootstrap.js",
                  "../js/animatescroll.js",
                  "../js/main.js",
                  "../js/plugins.js",
                  "../js/vendor/modernizr-2.8.3.min.js",
                  "../js/unslider.js",
                 ],
            dest:'../js/ugly.min.js',

        },
        dist: {
            options: {
                mangle: true,
                compress: true
            },
            src: ['../js/ugly.min.js'],
            dest: '../js/main.min.js'
        }
    },

    watch: {
        less: {
            files: ["./less/*.less"],
            tasks: ["less:development"],
            options: {
            },
        },
        concat: {
            files: ["*.css","!site.min.css", "!site.css"],
            tasks: ["concat"],
            options: {
                debounceDelay: 1500,
            },
        },

        cssmin: {
            files: ['site.css'],
            tasks: ['cssmin'],
            options: {
                debounceDelay: 1600,
            },
        },

        uglify: {
            files: ["../js/*.js"],
            tasks: ["uglify:dev"],
        }, 
    },

});
grunt.loadNpmTasks('grunt-contrib-less');
grunt.loadNpmTasks('grunt-contrib-watch');
grunt.loadNpmTasks('grunt-contrib-concat');
grunt.loadNpmTasks('grunt-contrib-cssmin');
grunt.loadNpmTasks('grunt-contrib-uglify');
grunt.loadNpmTasks('grunt-contrib-jshint');
grunt.registerTask( 'default', ['less','watch', 'concat', 'cssmin','jshint','uglify:dev'] );
};


