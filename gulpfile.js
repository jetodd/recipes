var gulp = require("gulp");
var livereload = require("gulp-livereload");
var exec = require("child_process").exec;

gulp.task("watch", function () {
  livereload.listen({ basePath: "recipes/static/recipes/" });
  gulp.watch("recipes/**/*").on("change", livereload.changed);
});

gulp.task("webserver", function () {
  var isWin = process.platform === "win32";
  var proc;
  if (isWin) {
    proc = exec("python manage.py runserver");
  } else {
    proc = exec("python3 manage.py runserver");
  }
  console.log("Server started on http://127.0.0.1:8000");
  proc.stderr.on("data", function (data) {
    process.stdout.write(data);
  });

  proc.stdout.on("data", function (data) {
    process.stdout.write(data);
  });
});

gulp.task("default", gulp.parallel("webserver", "watch"));
