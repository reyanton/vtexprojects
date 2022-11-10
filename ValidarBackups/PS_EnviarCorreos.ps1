function OpenConnection () {
    $Server = "ING-ICG05"
	$Database = "msdb"

    $sqlConnection = New-Object System.Data.SqlClient.SqlConnection
    $sqlConnection.ConnectionString = "server='$Server';database='$Database';trusted_connection=true;"

    $sqlConnection.Open()
    
    return $sqlConnection
}

function BuildHtmlBody ($sqlConnection) {
    
    $sqlQuery = "SELECT NameString,CreationTime,LastWriteTime,Status FROM [backupfiles] where LastWriteTime > dateadd(dd, -1, getdate())"
    $sqlCommand = New-Object System.Data.SqlClient.SqlCommand($sqlQuery, $sqlConnection);
    $reader = $sqlCommand.ExecuteReader()

    $html = "<!DOCTYPE html><html><body>"
    $html += "<div style=""font-family:'Segoe UI', Calibri, Arial, Helvetica; font-size: 14px; max-width: 768px;"">"
    $html +="<table style='border-spacing: 0px; border-style: solid; border-color: #ccc; border-width: 0 0 1px 1px;'>"

    while ($reader.Read()) {
        $Archivo = $reader.GetString(0)
        $Copiado = $reader.GetString(1)
        $Creado = $reader.GetString(2)
        $Estatus = $reader.GetString(3)

        $html += "<tr>"
        $html += "<td style='padding: 10px; border-style: solid; border-color: #ccc; border-width: 1px 1px 0 0;'>{0}</td>" -f $Archivo
        $html += "<td style='padding: 10px; border-style: solid; border-color: #ccc; border-width: 1px 1px 0 0;'>{0}</td>" -f $Copiado
        $html += "<td style='padding: 10px; border-style: solid; border-color: #ccc; border-width: 1px 1px 0 0;'>{0}</td>" -f $Creado
        $html += "<td style='padding: 10px; border-style: solid; border-color: #ccc; border-width: 1px 1px 0 0;'>{0}</td>" -f $Estatus
        $html += "</tr>"

    }

    $reader.Close > $null
    $reader.Dispose > $null

    $sqlCommand.Close > $null
    $sqlCommand.Dispose > $null

    return $html
}

$sqlConnection = OpenConnection
$bodyTemplate = BuildHtmlBody($sqlConnection);

$MsgBody = "Los siguientes respaldos fueron validados al : " + $(get-date -format dd-MM-yyyy) + "`n";
$MsgBody += $bodyTemplate

$Username = "rolbynet@hotmail.com";
$Password = "*-2007aveo-*";

function Send-ToEmail([string]$email, [string]$attachmentpath){

    $message = new-object Net.Mail.MailMessage;
    $message.From = "rolbynet@hotmail.com";
    $message.To.Add($email);
    $message.Subject = "Respaldos Revisados";
    $message.Body = $MsgBody;
	$message.IsBodyHTML = 1;
  
    $smtp = new-object Net.Mail.SmtpClient("smtp.live.com", "587");
    $smtp.EnableSSL = $true;
    $smtp.Credentials = New-Object System.Net.NetworkCredential($Username, $Password);
    $smtp.send($message);
	#Send-MailMessage -From $From -to $To -Subject $Subject -Body $MsgBody -BodyAsHTML -SmtpServer $SMTPServer -port $SMTPPort
    #write-host "Mail Sent" ; 
}

Send-ToEmail  -email "reinaldo.vanton@gmail.com;rolbynet@hotmail" 
		