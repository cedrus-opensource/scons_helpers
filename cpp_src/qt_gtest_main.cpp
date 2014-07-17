

#include <QApplication>

#include "UserInterface/UtilityClasses/MacCocoaQtHelpers.h"
#include <stdlib.h>

#include <QtWidgets/QMainWindow>
#include <QResource>
#include <QTimer>

#include <gtest/gtest.h>

/**
   the idea of using this 'Task' object was borrowed directly from here:

   http://stackoverflow.com/questions/4180394/how-do-i-create-a-simple-qt-console-application-in-c#4182144
 */
class Task : public QObject
{
    Q_OBJECT
public:
    Task(QObject *parent = 0) : QObject(parent) {}

    virtual ~Task()
    {}

public Q_SLOTS:
    void run()
    {
        int ret = RUN_ALL_TESTS();
        qApp->exit( ret );
    }
};

#include "qt_gtest_main_mocout.cpp"


/**
   this is here so that we can override the 'notify' function, if we decide we need to
 */
class TestRunnerApp : public QCoreApplication
{
public:
    TestRunnerApp(int &argc, char **argv )
        : QCoreApplication( argc, argv )
    {}


    //virtual bool notify(QObject * o, QEvent *e);

private:
};




#ifdef __APPLE__

int main(int argc, char *argv[])
{
    // the following MUST BE DONE *prior* to the 'addLibraryPath':
    QCoreApplication::setOrganizationName("Cedrus"); // this ENABLES cedrus-specific code INSIDE the Qt libraries! crucial!

    std::string app_bundle = Cedrus::GetMacAppBundlePath();

    const QString bundle_path = QString::fromUtf8( app_bundle.c_str(), app_bundle.size() );//  [string UTF8String]);
    QCoreApplication::addLibraryPath( bundle_path );

#elif defined(_WIN32)

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    QCoreApplication::setOrganizationName("Cedrus"); // this ENABLES cedrus-specific code INSIDE the Qt libraries! crucial!

    char wargv[10];
    char * pargv = wargv;
    char ** argv = &pargv;
    int argc = 0;
#endif //#ifdef __APPLE__

    testing::InitGoogleTest(&argc, argv);

    TestRunnerApp app(argc, argv);

    // Task parented to the application so that it
    // will be deleted by the application.
    Task *task = new Task(&app);

    // This will run the task from the application event loop.
    QTimer::singleShot(0, task, SLOT(run()));

    return app.exec();
}


/*

void TestRunnerApp::OnFatalException()
{
	GTEST_FATAL_FAILURE_("This");
	wxTrap();
}


void TestRunnerApp::OnAssertFailure(const wxChar *szFile,
									int nLine,
									const wxChar* WXUNUSED(szFunc),
									const wxChar* WXUNUSED(szCond),
									const wxChar *szMsg)
{
	// just swallow asserts.  We want to ignore them in Unit Tests
	// I'll be nice and at least print a message to stdout, though.
	wxString fileString( szFile );
	std::string file( fileString.mb_str( wxConvUTF8 ) );
	std::cout << "An Assert happened in " << file << " at line " << nLine << std::endl;
	wxString message( szMsg );
	std::string stdMessage( message.mb_str( wxConvUTF8 ) );
	std::cout << "Assert Message: " << stdMessage << std::endl;
}


*/
