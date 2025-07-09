import datetime

def nanosecond_unix_to_datetime_string(nanosecond_timestamp, format_string="%Y-%m-%d %H:%M:%S.%f"):
    """
    ナノ秒単位のUNIXタイムスタンプを文字列の日時に変換します。

    Args:
        nanosecond_timestamp (int): ナノ秒単位のUNIXタイムスタンプ。
        format_string (str): 出力する日時のフォーマット文字列。
                             %f はマイクロ秒を表しますが、ナノ秒の情報も含まれるように処理します。

    Returns:
        str: フォーマットされた日時文字列。
    """
    if not nanosecond_timestamp:
        return ""
    # まず、秒と残りのナノ秒に分割します
    # Pythonのdatetimeはマイクロ秒までの精度なので、ナノ秒をマイクロ秒に変換します
    seconds = nanosecond_timestamp // 1_000_000_000  # 秒
    remaining_nanoseconds = nanosecond_timestamp % 1_000_000_000 # 残りのナノ秒

    # マイクロ秒に変換
    microseconds = remaining_nanoseconds // 1_000 # ナノ秒をマイクロ秒に

    # datetimeオブジェクトを作成
    dt_object = datetime.datetime.fromtimestamp(seconds)
    dt_object = dt_object.replace(microsecond=microseconds)

    # フォーマットして文字列として返す
    # %f はマイクロ秒までしか表示しませんが、この方法で最も近い表現ができます。
    # 必要に応じて、ナノ秒を別の方法で文字列に付加することも検討できます。
    return dt_object.strftime(format_string)

