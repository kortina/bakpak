#!/usr/bin/env bash
# via: http://apple.stackexchange.com/questions/108171/export-imessages-in-human-readable-form-for-archival

# Usage:
# ./imessage-transcript.sh "+12223334444"
# Parameter is a iMessage account (email or phone, eg  +12223334444 )
if [ $# -lt 1 ]; then
    echo "Enter a iMessage account (email of phone, eg  +12223334444) "
fi
login=$1
stripped_login=`echo "$login" | perl -pe 's/\W/-/'`
transcript_filename="imessage-transcript-$stripped_login.txt"

# Retrieve the text messages 

echo -e "imessage transcript for: $login\n" > $transcript_filename
sqlite3 ~/Library/Messages/chat.db "
select is_from_me,text from message where handle_id=(
select handle_id from chat_handle_join where chat_id=(
select ROWID from chat where guid='iMessage;-;$1')
)" | sed 's/1\|/me: /g;s/0\|/buddy: /g' >> $transcript_filename
cat $transcript_filename


# Retrieve the attached stored in the local cache

sqlite3 ~/Library/Messages/chat.db "
select filename from attachment where rowid in (
select attachment_id from message_attachment_join where message_id in (
select rowid from message where cache_has_attachments=1 and handle_id=(
select handle_id from chat_handle_join where chat_id=(
select ROWID from chat where guid='iMessage;-;$1')
)))" | cut -c 2- | awk -v home=$HOME '{print home $0}' | tr '\n' '\0' | xargs -0 -t -I fname cp fname .
