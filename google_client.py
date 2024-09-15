import os
from googleapiclient.discovery import build
from pydantic import BaseModel, Field


class GoogleSearchQueryParameter(BaseModel):
    """
    Google Custom Search APIの検索クエリパラメータを表すクラス
    https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list?hl=ja

    Args:
        num: 取得する検索結果の最大数
        start: 検索結果の開始位置
        lr: 言語
        sort: ソート方法
        fileType: 特定のファイルタイプに限定
        dateRestrict: 特定の期間内の結果に限定
        siteSearch: 特定のサイト内での検索
        exactTerms: 完全一致で検索するキーワード
        excludeTerms: 除外するキーワード
    """
    num: int | None = Field(default=10, ge=1, le=100)
    start: str | None = Field(default=None)
    lr: str | None = Field(default="lang_ja")
    sort: str | None = Field(default=None)
    dateRestrict: str | None = Field(default=None)
    exactTerms: str | None = Field(default=None)
    excludeTerms: str | None = Field(default=None)
    safe: str | None = Field(default=None)


class GoogleClient:
    def __init__(self, api_key: str | None = None, cse_id: str | None = None):
        """
        Google Custom Search APIを利用するためのクライアントクラス

        Args:
            api_key: API Key
            cse_id: Search Engine ID
        """
        if not api_key:
            api_key = os.getenv("CUSTOM_SEARCH_API_KEY")
        if not cse_id:
            cse_id = os.getenv("SEARCH_ENGINE_ID")

        self.custom_search_api_key = api_key
        self.cse_id = cse_id

    def search(self, query: str, **kwargs):
        """
        Google Custom Search APIを利用して検索を実行

        Args:
            query: 検索語
            **kwargs: 検索クエリパラメータ
        """
        service = build("customsearch", "v1",
                        developerKey=self.custom_search_api_key)
        res = service.cse().list(q=query, cx=self.cse_id, **kwargs).execute()
        return res['items']

    def search_query_parameter(
            self, num: int = 10, start: str = None, lr: str = "lang_ja",
            sort: str = None, dateRestrict: str = None, exactTerms: str = None,
            excludeTerms: str = None, safe: str = None):
        """
        Google Custom Search APIの検索クエリパラメータを表すクラス
        https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list?hl=ja

        Args:
            num: 取得する検索結果の最大数
            start: 検索結果の開始位置
            lr: 言語
            sort: ソート方法
            fileType: 特定のファイルタイプに限定
            dateRestrict: 特定の期間内の結果に限定
            siteSearch: 特定のサイト内での検索
            exactTerms: 完全一致で検索するキーワード
            excludeTerms: 除外するキーワード
        """
        # クエリパラメータを設定
        query_parameter = GoogleSearchQueryParameter(
            num=num, start=start, lr=lr, sort=sort, dateRestrict=dateRestrict,
            exactTerms=exactTerms, excludeTerms=excludeTerms, safe=safe)

        return {
            k: v for k, v in query_parameter.model_dump().items() if v is not None
        }


if __name__ == "__main__":
    import pprint

    # 検索語を設定
    query = "Python programming"

    # クライアントを生成
    client = GoogleClient()

    # 検索を実行
    results = client.search(query)

    # 結果を表示
    for item in results:
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Snippet: {item['snippet']}")
        print("---")

    # 詳細な結果を表示したい場合は以下のコメントを解除してください
    pprint.pprint(results)
