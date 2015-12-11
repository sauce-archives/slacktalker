exec = require('child_process').exec

endpoint = 'foo.com:80'

module.exports = (robot) ->
  robot.respond /resurrect (.*)$/i, (msg) ->
    username = msg.match[1]
    child = exec 'curl -s http://' + endpoint + '/generate/' + username + '/', (error, stdout, stderr) ->
      if stderr
        msg.send "stderr: #{stderr}"
      msg.send stdout
      if error
        msg.send "exec error: #{error}"
  robot.respond /talker list users$/i, (msg) ->
    child = exec 'curl -s http://' + endpoint + '/users/', (error, stdout, stderr) ->
      if stderr
        msg.send "stderr: #{stderr}"
      msg.send stdout
      if error
        msg.send "exec error: #{error}"
