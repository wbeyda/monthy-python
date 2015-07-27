module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        
        less: {
          development: {
          options: {
                paths: ["less/"]
            },
            
            files: {
                "style.css": "less/style.less"
            }
          }
        },
        watch: {
            files: "less/**/*.less",
            tasks: ["less"]
        }
    })
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask( 'default', ['less','watch'] );
};

