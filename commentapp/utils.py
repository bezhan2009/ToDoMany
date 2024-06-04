from commentapp.serializers import CommentsSerializer


def build_comment_tree(comment, comments_dict):
    comment_data = CommentsSerializer(instance=comment).data
    children_comments = comments_dict.get(comment.id, [])

    if children_comments:
        comment_data['children'] = [build_comment_tree(
            child,
            comments_dict
        ) for child in children_comments]

    return comment_data
