# NNI���C���|�[�g����
import nni
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder


def load_data(train_file_path):
    """
    �f�[�^�̑O�������s���֐�
    Parameters
    ----------
    train_file_path : str
        �w�K�p�f�[�^�̃t�@�C���p�X
    Returns
    -------
    X_train : pd.DataFrame
        �w�K�p�̃f�[�^
    y_train : Series
        �w�K�p�̐������x��
    """
    train_df = pd.read_csv(train_file_path)
    y_train = train_df.pop('Survived')
    X_train = train_df.drop(['PassengerId', 'Name'], axis=1)
    list_cols = ['Sex', 'Ticket', 'Cabin', 'Embarked']
    for col in list_cols:
        le = LabelEncoder()
        le.fit(X_train[col])
        X_train[col] = le.transform(X_train[col])
    return X_train, y_train


def get_default_parameters():
    """
    �f�t�H���g�̃p�����[�^�[���擾����֐�
    Returns
    -------
    params : dict
        �f�t�H���g�̃p�����[�^�[
    """
    params = {
        'learning_rate': 0.02,
        'n_estimators': 2000,
        'max_depth': 4,
        'min_child_weight': 2,
        'gamma': 0.9,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'objective': 'binary:logistic',
        'nthread': -1,
        'scale_pos_weight': 1
    }
    return params


def get_model(PARAMS):
    """
    ���f������肷��֐�
    Parameters
    ----------
    PARAMS : dict
        �p�����[�^�[
    Returns
    -------
    model : xgboost.sklearn.XGBClassifier
        �w�K�Ɏg�p���郂�f��
    """
    model = xgb.XGBClassifier()
    model.learning_rate = PARAMS.get("learning_rate")
    model.max_depth = PARAMS.get("max_depth")
    model.subsample = PARAMS.get("subsample")
    model.colsample_btree = PARAMS.get("colsample_btree")
    return model


def run(X_train, y_train, model):
    """
    ���f�������s����֐�
    Parameters
    ----------
    X_train : pd.DataFrame
        �w�K�p�̃f�[�^
    y_train : pd.DataFrame
        �w�K�p�̐������x��
    model : xgboost.sklearn.XGBClassifier
        �w�K�Ɏg�p���郂�f��
    """
    scores = cross_val_score(model, X_train, y_train,
                             scoring='accuracy', cv=KFold(n_splits=5))
    score = scores.mean()
    # Configuration�̌��ʂ�񍐂���
    nni.report_final_result(score)


if __name__ == '__main__':
    X_train_sub, y_train_sub = load_data('train.csv')
    # Tuner����Configuration���擾����
    RECEIVED_PARAMS = nni.get_next_parameter()
    PARAMS = get_default_parameters()
    PARAMS.update(RECEIVED_PARAMS)
    model = get_model(PARAMS)
    run(X_train_sub, y_train_sub, model)
